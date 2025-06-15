import jinja2
import sys


def render(issue_no: int) -> str:
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader("templates"), autoescape=True
    )
    template = env.get_template("newsletter.html.j2")
    html = template.render(issue=issue_no)
    return html


if __name__ == "__main__":
    print(render(int(sys.argv[1])))
