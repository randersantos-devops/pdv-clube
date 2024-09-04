from django.db import models

from escpos.printer import Usb


class InviteType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, verbose_name='Nome')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço')

    def __str__(self):
        return self.name

class InviteSale(models.Model):

    FORMAS_DE_PAGAMENTO = [
        ('CRÉDITO', 'CRÉDITO'),
        ('DÉBITO', 'DÉBITO'),
        ('DINHEIRO', 'DINHEIRO'),
        ('PIX', 'PIX'),
    ]

    id = models.AutoField(primary_key=True, verbose_name='COD')
    dt_retired = models.DateTimeField(auto_now_add=True, verbose_name='Data de Retirada')
    type_invite = models.ForeignKey(InviteType, on_delete=models.CASCADE, verbose_name='Tipo de Convite')
    name_guest = models.CharField(max_length=255, verbose_name='Nome do Convidado')
    doc_guest = models.CharField(max_length=15, verbose_name='Documento do Convidado')
    forma_de_pagamento = models.CharField(max_length=100, choices=FORMAS_DE_PAGAMENTO, verbose_name='Forma de Pagamento')
    observation = models.TextField(null=True, blank=True, verbose_name='Observações')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        ordering = ['dt_retired']
        verbose_name = 'Convite Vendido'
        verbose_name_plural = 'Convites Vendidos'

    def __str__(self):
        return f'Comprado por: {self.name_associate} em {self.dt_retired}'
    
    def generate_voucher(self):
        p = Usb(0x04B8, 0x0E27, 0, 0, 0)  # Substitua pelos IDs corretos da sua impressora

        cabecalho = '''CLUBE STIQUIFAR - CNPJ:20.052.817/0001-10\n\n
        TELEFONE: (34)3317-1646 - R. OUTONO 150, VILA ARQUELAU - UBERABA/MG
        '''
        logo = r'C:\Users\stiqu\PDV-CLUBE\django_admin\static\img\logo-stiquifar-site-recibo.png'

        p.set(align='center')
        p.image(img_source=logo)
        p.ln(1)
        p.set(bold=True, align='left')
        p.block_text(cabecalho)
        p.ln(2)
        p.set(height= 4, width= 4)    
        p.text("Comprovante Convite Vendido")
        p.ln(2)
        p.set(height= 2, width= 2, bold=False)
        p.text(f'Convidado: {self.name_guest}\n')
        p.text(f'Tipo de Convite: {self.type_invite.name}\n')
        p.text(f'Doc Convidado: {self.doc_guest}\n')
        p.text(f'Data de Retirada: {self.dt_retired.strftime("%d/%m/%Y %H:%M:%S")}\n')
        p.text(f'Valor Pago: R$ {self.type_invite.price}\n')
        p.text(f'Forma de Pagamento: {self.get_forma_de_pagamento_display()}')
        if self.observation:
            p.text(f'Observação: {self.observation}\n')
        p.ln(2)
        p.set(height=4, width=4, bold=True)
        p.text('Obrigado por visitar o Clube Stiquifar!!')
        p.cut()

    def __str__(self):
        return f'Comprado por: {self.name_guest}'