from django import forms

from app.ip1sms import SMSGateway
from app.models import ClientProxy

sms = SMSGateway()

class SMSAnnouncementForm(forms.ModelForm):
    message = forms.CharField(
            required=True,
            widget=forms.Textarea,
        )

    class Meta:
        model = ClientProxy
        fields = "__all__"

    # def form_action(self):
    #     raise NotImplementedError()
    #
    # def save(self):
    #     clients = Client.objects.all()
    #     for client in clients:
    #         sms.sendMessage(client.phone, self.message)
