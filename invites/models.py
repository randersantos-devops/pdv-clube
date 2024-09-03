from django.db import models

from escpos.printer import Usb

class Invite(models.Model):

    TYPE_ASSOCIATES = [
        ('AGREGADO', 'AGREGADO(a)'),
        ('SINDICALIZADO', 'SINDICALIZADO(A)'),
    ]

    STATUS_INVITES = [
        ('RETIRADO', 'RETIRADO'),
        ('SOLICITADO', 'SOLICITADO'),
    ]

    id = models.AutoField(primary_key=True, verbose_name='COD')
    dt_retired = models.DateTimeField(auto_now_add=True, verbose_name='Data de Retirada')
    name_associate = models.CharField(max_length=255, verbose_name='Nome do Titular')
    type_associate = models.CharField(max_length=30, choices=TYPE_ASSOCIATES, verbose_name='Tipo de Sócio')
    name_guest = models.CharField(max_length=255, verbose_name='Nome do Convidado')
    doc_guest = models.CharField(max_length=15, verbose_name='Documento do Convidado')
    status_invite = models.CharField(max_length=30, choices=STATUS_INVITES, verbose_name='Status do Convite',default='SOLICITADO')
    observation = models.TextField(null=True, blank=True, verbose_name='Observações')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')

    class Meta:
        ordering = ['dt_retired']
        verbose_name = 'Convite'
        verbose_name_plural = 'Convites'

    def __str__(self):
        return f'Retirado por: {self.name_associate} em {self.dt_retired}'
    
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
        p.text("Comprovante Cortesia")
        p.ln(2)
        p.set(height= 2, width= 2, bold=False)
        p.text(f'Titular: {self.name_associate}\n')
        p.text(f'Tipo de Associado: {self.get_type_associate_display()}\n')
        p.text(f'Convidado: {self.name_guest}\n')
        p.text(f'Doc Convidado: {self.doc_guest}\n')
        p.text(f'Data de Retirada: {self.dt_retired.strftime("%d/%m/%Y %H:%M:%S")}\n')
        if self.observation:
            p.text(f'Observação: {self.observation}\n')
        p.ln(2)
        p.set(height=4, width=4, bold=True)
        p.text('Obrigado por visitar o Clube Stiquifar!!')
        p.cut()

    def __str__(self):
        return f'Convidado de: {self.name_associate}'