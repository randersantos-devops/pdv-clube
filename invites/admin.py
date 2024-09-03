from django.utils.html import format_html
from django.contrib import admin
from django.urls import path, reverse
from django.shortcuts import redirect, get_object_or_404
from django.utils.timezone import localtime, make_aware, get_current_timezone

# Importação Minha
from .models import Invite

@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    list_display = ['formatted_dt_retired', 'name_associate', 'type_associate', 'name_guest', 'doc_guest', 'gerar_comprovante_button']
    readonly_fields = ['gerar_comprovante_button']

    def formatted_dt_retired(self, obj):
        if obj.dt_retired:
            aware_dt_retired = make_aware(obj.dt_retired, get_current_timezone()) if obj.dt_retired.tzinfo is None else obj.dt_retired
            formatted_date = localtime(aware_dt_retired).strftime('%d/%m/%Y %H:%M:%S')
            return format_html('<span>{}</span>', formatted_date)
        return '-'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:invite_id>/gerar_comprovante/', self.admin_site.admin_view(self.gerar_comprovante), name='gerar_comprovante'),
        ]
        return custom_urls + urls

    def gerar_comprovante(self, request, invite_id):
        cortesia = get_object_or_404(Invite, pk=invite_id)
        try:
            # Chamando o método que gera o comprovante
            cortesia.generate_voucher()
            self.message_user(request, "Comprovante gerado com sucesso.")
        except Exception as e:
            self.message_user(request, f"Erro ao gerar o comprovante: {str(e)}", level='error')
        return redirect('/admin/invites/invite/')

    def gerar_comprovante_button(self, obj):
        if obj.pk:  # Verifica se o objeto já foi salvo
            url = reverse('admin:gerar_comprovante', args=[obj.pk])
            return format_html('<a class="button" href="{}">Gerar Comprovante</a>', url)
        return "Salve a cortesia para gerar o comprovante"

    gerar_comprovante_button.short_description = 'Gerar Comprovante'
