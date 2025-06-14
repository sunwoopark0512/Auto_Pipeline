import json
import datetime
import sys
from jinja2 import Environment, FileSystemLoader

DATA = "data/generated_hooks.json"
TEMPLATE = "templates/newsletter.html.j2"


def main(limit: int = 10):
    env = Environment(loader=FileSystemLoader("templates"))
    tpl = env.get_template("newsletter.html.j2")
    keywords = json.loads(open(DATA, encoding="utf-8").read())[:limit]
    html = tpl.render(date=datetime.date.today(), keywords=keywords)
    open("newsletter_out.html", "w", encoding="utf-8").write(html)
    print("newsletter_out.html generated")


if __name__ == "__main__":
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    main(limit)
