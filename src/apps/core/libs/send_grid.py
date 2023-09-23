from mailjet_rest import Client
import os
from typing import List

class SendMailJet:

    API_KEY = 'aa5b1feb5ff0b21ed1eabae0a52f031c'
    API_SECRET = '509d0b092fc771aaa542b759de5b0967'
    FROM_EMAIL = "contact@infinitymgt.fr" # 'no-reply@lprs.com' #

    @classmethod
    def send_mail(cls, emails: List[str], subject: str, html: str,
                  attached_content: bytes = None,file_name: str = None):
        # encoded_file = open(attached_content, "rb").read().encode("base64")
        # attached_content=attached_content.decode('utf16')
        print(attached_content,'=====================================')
        if attached_content:
            data = {
                'Messages': [
                    {
                        "From": {
                            "Email": cls.FROM_EMAIL,
                            "Name": "E-Hiring team"
                        },
                        "To": [{"Email": email} for email in emails],
                        "Subject": subject,
                        "TextPart": "My first Mailjet email",
                        "HTMLPart": html,
                        "CustomID": "AppGettingStartedTest",
                        "Attachments": [
                            {
                                "ContentType": "application/pdf",
                                "Filename": file_name,
                                "Base64Content": attached_content,
                            }
                        ]
                    }
                ]
            }
        else:
            data = {
                'Messages': [
                    {
                        "From": {
                            "Email": cls.FROM_EMAIL,
                            "Name": "E-Hiring team"
                        },
                        "To": [{"Email": email} for email in emails],
                        "Subject": subject,
                        "TextPart": "My first Mailjet email",
                        "HTMLPart": html,
                        "CustomID": "AppGettingStartedTest",
                    }
                ]
            }

        print(data)

        mailjet = Client(auth=(cls.API_KEY, cls.API_SECRET), version='v3.1')
        #sg = SendGridAPIClient(cls.API_KEY)
        try:
            #response = sg.send(message)
            result = mailjet.send.create(data=data)
            print(result.status_code)
            print(result.json())
            return result
        except Exception as error:
            print(error)


















# # Using SendGrid's Python Library
# # https://github.com/sendgrid/sendgrid-python
# from typing import List
# from django.conf import settings
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail, Attachment, \
#     FileContent, FileName, FileType, Disposition
#
#
# class SendGrid:
#     API_KEY = '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'
#     FROM_EMAIL = 'no-reply@lprs.com'
#
#     @classmethod
#     def send_mail(cls, email: List[str], subject: str, html: str,
#                   attached_content: bytes = None):
#         # if settings.DEBUG:
#         #     from django.core.mail import send_mail
#         #
#         #     return send_mail(
#         #         subject=subject,
#         #         html_message=html,
#         #         message=html,
#         #         from_email=cls.FROM_EMAIL,
#         #         recipient_list=email,
#         #         fail_silently=False,
#         #     )
#
#
#         message = Mail(
#             from_email=cls.FROM_EMAIL,
#             to_emails=email,
#             subject=subject,
#             html_content=html
#         )
#         sg = SendGridAPIClient(cls.API_KEY)
#         try:
#             response = sg.send(message)
#         except Exception as error:
#             print(error)
#         else:
#             return response
