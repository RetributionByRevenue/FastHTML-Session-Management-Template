from fasthtml.common import *

def generate_homepage_content(username, login_time):
    """
    Generate the HTML content for the homepage.

    Args:
        username (str): The username of the logged-in user.
        login_time (str): The formatted login time of the user.

    Returns:
        tuple: A tuple containing the title and main content for the homepage.
    """
    title = f"Welcome {username}"

    top = Grid(
        H1(title),
        Div(
            A('Logout', href='/logout'),
            style='text-align: right'
        )
    )

    content = Article(
        H2("Dashboard"),
        P("This is the protected main page. Only authenticated users can see this content."),
        P(f"Login Time: {login_time}"),
        cls='container'
    )

    return Title(title), Main(top, content)
