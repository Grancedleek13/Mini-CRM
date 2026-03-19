import json

from django.contrib import messages
from django.db.models import Count, Q
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import LeadForm, LeadStatusForm
from .models import Lead


@require_http_methods(['GET'])
def dashboard(request: HttpRequest):
    selected_status = request.GET.get('status', '')
    search_query = request.GET.get('q', '').strip()

    leads = Lead.objects.all()

    if selected_status:
        leads = leads.filter(status=selected_status)

    if search_query:
        leads = leads.filter(Q(full_name__icontains=search_query) | Q(phone__icontains=search_query))

    counters = dict(Lead.objects.values_list('status').annotate(total=Count('id')))
    stats = {
        'total': Lead.objects.count(),
        'new': counters.get(Lead.Status.NEW, 0),
        'in_progress': counters.get(Lead.Status.IN_PROGRESS, 0),
        'done': counters.get(Lead.Status.DONE, 0),
    }

    return render(
        request,
        'leads/dashboard.html',
        {
            'leads': leads,
            'form': LeadForm(),
            'status_form': LeadStatusForm(),
            'selected_status': selected_status,
            'search_query': search_query,
            'status_choices': Lead.Status.choices,
            'stats': stats,
        },
    )


@require_http_methods(['POST'])
def create_lead(request: HttpRequest):
    form = LeadForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Заявка добавлена.')
    else:
        messages.error(request, 'Не удалось сохранить заявку. Проверьте поля формы.')
    return redirect('dashboard')


@require_http_methods(['POST'])
def update_status(request: HttpRequest, lead_id: int):
    lead = get_object_or_404(Lead, id=lead_id)
    form = LeadStatusForm(request.POST, instance=lead)
    if form.is_valid():
        form.save()
        messages.success(request, f'Статус заявки «{lead.full_name}» обновлён.')
    else:
        messages.error(request, 'Статус не был обновлён.')
    return redirect('dashboard')


@require_http_methods(['GET', 'POST'])
def api_leads(request: HttpRequest):
    if request.method == 'GET':
        data = [serialize_lead(lead) for lead in Lead.objects.all()]
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})

    payload = parse_json_body(request)
    required_fields = ['full_name', 'phone']
    missing_fields = [field for field in required_fields if not payload.get(field)]

    if missing_fields:
        return JsonResponse(
            {'error': f'Не заполнены обязательные поля: {", ".join(missing_fields)}'},
            status=400,
            json_dumps_params={'ensure_ascii': False},
        )

    lead = Lead.objects.create(
        full_name=payload.get('full_name', '').strip(),
        phone=payload.get('phone', '').strip(),
        email=payload.get('email', '').strip(),
        company=payload.get('company', '').strip(),
        source=payload.get('source') or Lead.Source.WEBSITE,
        budget=payload.get('budget') or None,
        comment=payload.get('comment', '').strip(),
    )
    return JsonResponse(serialize_lead(lead), status=201, json_dumps_params={'ensure_ascii': False})


@require_http_methods(['GET', 'PATCH'])
def api_lead_detail(request: HttpRequest, lead_id: int):
    lead = get_object_or_404(Lead, id=lead_id)

    if request.method == 'GET':
        return JsonResponse(serialize_lead(lead), json_dumps_params={'ensure_ascii': False})

    payload = parse_json_body(request)
    new_status = payload.get('status')
    valid_statuses = {choice[0] for choice in Lead.Status.choices}

    if new_status not in valid_statuses:
        return JsonResponse(
            {'error': 'Передан некорректный статус.'},
            status=400,
            json_dumps_params={'ensure_ascii': False},
        )

    lead.status = new_status
    lead.save(update_fields=['status', 'updated_at'])
    return JsonResponse(serialize_lead(lead), json_dumps_params={'ensure_ascii': False})


def serialize_lead(lead: Lead) -> dict:
    return {
        'id': lead.id,
        'full_name': lead.full_name,
        'phone': lead.phone,
        'email': lead.email,
        'company': lead.company,
        'source': lead.source,
        'source_label': lead.get_source_display(),
        'budget': lead.budget,
        'status': lead.status,
        'status_label': lead.get_status_display(),
        'comment': lead.comment,
        'created_at': lead.created_at.strftime('%d.%m.%Y %H:%M'),
        'updated_at': lead.updated_at.strftime('%d.%m.%Y %H:%M'),
    }


def parse_json_body(request: HttpRequest) -> dict:
    try:
        return json.loads(request.body.decode('utf-8') or '{}')
    except json.JSONDecodeError:
        return {}
