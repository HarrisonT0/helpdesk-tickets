from ..database import db
from ..models.user import User
from ..models.ticket import Ticket
from ..models.comment import Comment
from werkzeug.security import generate_password_hash

company_domain = "company.com"
names = [
    "alice",
    "bob",
    "james",
    "luther",
    "bruce",
    "jeff",
    "andrew",
    "louis",
    "mike",
    "gerald",
]
tickets = {
    "ArgoCD": "I have setup ArgoCD in my cluster but cannot connect to it, I think there are some upstream network issues that may need investigating",
    "AWS Logged Out": "I have been logged out of my AWS account and when I try and log back in, for some reason, it does not let me. It is as if the account has been deleted or something. The account was registered under my corporate email (the one attached to this ticket). Please investigate.",
    "IP Ranges": "I am wondering where I can find the corporate IP ranges so I can properly configure a WAF for my webapp, I couldn't find it in the docs anywhere! Thanks :)",
    "Flask": "Any flask specialists in the IT team? My templates aren't rendering correctly and I am getting '500 internal server error' when I try and hit one of my routes.",
    "Coffee Machine": "The coffee machine is broken! It has a screen on it so I imagine it comes under the IT support team's remit",
    "Password reset on system": "I have forgotten my password on our corporate intranet, please reset it for me. thanks",
    "Laptop broken": "My work laptop will no longer turn on and I am not entirely sure why. I think I will need a new one or at least a temporary one whilst this one gets fixed, as I have critical work that I need to get on with in the meantime. Please get back to me with instructions on how I can book a pickup for a new laptop and give this broken one in",
    "Database connectivity": "I cannot connect to our HR database from my node which should be in the same network and subnet, it seems to be a connectivity issue, I am not sure if there is some sort of whitelist or if I need to request access. Please let me know - thanks.",
    "Keyboard broken": "The desk at my keyboard is broken, and I will need a replacement to use my work machine.",
    "Password reset": "I have been logged out of my work laptop and forgotten the password, please reset, thanks",
}
comments = {
    "ArgoCD": [
        {
            "admin": "Network benchmarks are coming back OK, are you sure you have configured everything correctly?"
        },
        {
            "user": "Configuration looks to be valid to me - cannot hit the node via telnet however"
        },
        {
            "admin": "I will forward you an email with the requirements for connectivity. Please check against them and reply if you can get things working. I will then close this ticket. Thanks."
        },
    ],
    "Coffee Machine": [
        {
            "admin": "This is not the correct place for such tickets - please raise this with the estates team instead of the IT helpdesk!"
        }
    ],
    "Password reset on system": [
        {
            "admin": "I have sent you a password reset email. Once we are notified your password update has gone through, I will come back and close this ticket as resolved. Thanks."
        },
        {
            "user": "Great, I'll check that email out in a short while, thanks very much for sending that over"
        },
    ],
    "Keyboard broken": [
        {
            "admin": "I have ordered in a new keyboard and it is ready for your collection at our desk. I will close this ticket as resolved once you have collected it. Thanks."
        },
        {
            "user": "That's brilliant, thank you very much. What times are you open on Wednesday?"
        },
        {
            "admin": "Unfortunately our in-person services are not available on Wednesdays - sorry. We will be open on Thursday from 9am - 6pm, if that works for you?"
        },
        {
            "user": "No worries - I will pick it up on Thursday morning. Thanks for your help again."
        },
    ],
}


def seed_database():
    # Create admin
    admin_email = f"admin@{company_domain}"
    admin_user = User.query.filter_by(email=admin_email).first()
    if not admin_user:
        admin_user = User(
            email=admin_email,
            password_hash=generate_password_hash("Password123!"),
            admin=True,
        )
        db.session.add(admin_user)

    # Create users, tickets and comments
    for index, name in enumerate(names):
        # Create user
        email = f"{name}@{company_domain}"
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(
                email=email,
                password_hash=generate_password_hash("Password123!"),
            )
            db.session.add(user)

        # Create user ticket
        title = list(tickets)[index]
        content = list(tickets.values())[index]
        ticket = Ticket.query.filter_by(title=title).first()
        if not ticket:
            ticket = Ticket(title=title, content=content, author_id=user.id)
            db.session.add(ticket)

        # Create ticket comments (if any)
        ticket_comments = comments.get(title)
        if ticket_comments:
            for ticket_comment in ticket_comments:
                if not Comment.query.filter_by(
                    content=list(ticket_comment.values())[0]
                ).first():
                    comment_author_id = (
                        admin_user.id if list(ticket_comment)[0] == "admin" else user.id
                    )
                    comment = Comment(
                        content=list(ticket_comment.values())[0],
                        ticket_id=ticket.id,
                        author_id=comment_author_id,
                    )
                    db.session.add(comment)

    db.session.commit()
