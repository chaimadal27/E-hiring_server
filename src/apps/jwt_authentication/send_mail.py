from django.template import loader

from apps.core.libs.send_grid import SendMailJet

from .settings import SETTINGS


def send_mail_on_create_new_account(user):

    reset_password_link = SETTINGS.RESET_PASSWORD_LINK.format(user.confirm_token)

    # TODO TO change config message
    message = "Bienvenue au E-Hiring , votre compte a été créé avec succès . \n" \
        f" Voici le lien pour mettre à jour votre mot de passe: <a href='{reset_password_link}'>Cliquez ici</a> ." \
        f"Votre profile est: {user.email}."

    import pprint
    pp = pprint.PrettyPrinter(depth=6)
    pp.pprint('**********************************')
    pp.pprint(f'{SETTINGS.RESET_PASSWORD_LINK.format(user.confirm_token)}')
    pp.pprint('**********************************')

    message_html = loader.render_to_string(
        'base_auth_mail.html',
        {'user': user, 'reset_password_link': reset_password_link, 'message': message}
    )

    SendMailJet.send_mail(
        [user.email, ],
        subject="Bienvenue au E-Hiring",
        html=message_html
    )


def send_mail_on_frogot_password(user):

    reset_password_link = SETTINGS.RESET_PASSWORD_LINK.format(user.confirm_token)
    # TODO TO change config message
    message = "Bienvenue au E-Hiring , Vous avez oublié votre mot de passe . \n" \
        f" Voici votre link pour mettre à jour votre mot de passe:<a href='{reset_password_link}'>Cliquez ici</a>." \
        f"Votre profile est: {user.email}."

    import pprint
    pp = pprint.PrettyPrinter(depth=6)
    pp.pprint('**********************************')
    pp.pprint(user.email)
    pp.pprint('**********************************')

    message_html = loader.render_to_string(
        'base_auth_mail.html',
        {'user': user, 'reset_password_link': reset_password_link, 'message': message}
    )

    SendMailJet.send_mail(
        [user.email, ],
        subject="Bienvenue au E-Hiring",
        html=message_html
    )


def send_mail_on_update_account(user):

    message = "Bienvenue au E-Hiring , votre compte a été modifié avec succès ."
    message_html = loader.render_to_string('base_auth_mail.html', {'user': user, 'message': message})

    SendMailJet.send_mail(
        [user.email, ],
        subject="Bienvenue au E-Hiring",
        html=message_html
    )


def send_mail_on_password_reset(user):

    message = "Bienvenue au E-Hiring , votre mot de passe a été modifié avec succès ."
    message_html = loader.render_to_string('base_auth_mail.html', {'user': user, 'message': message})

    SendMailJet.send_mail(
        [user.email, ],
        subject="Bienvenue au E-Hiring",
        html=message_html
    )

def send_mail_on_share_candidate_cv(user,users,file,file_name):

    message = f"Bienvenue au E-Hiring , <b>{user.email}</b>  souhaite partager avec vous un candidat. \n" \
        " Vous trouverez ci-joint son curriculum-vitae." \

    message_html = loader.render_to_string('base_auth_mail.html', {'user': user, 'message': message})
    users_emails=[user.email for user in users]
    SendMailJet.send_mail(
        users_emails,
        subject="Bienvenue au E-Hiring",
        html=message_html,
        attached_content=file,
        file_name=file_name
    )