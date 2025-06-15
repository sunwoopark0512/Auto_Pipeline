"""Example dynamic pipeline step registry."""


def gen_keywords():
    """Generate keyword list for content."""
    print("Generating keywords")


def write_article():
    """Write article content."""
    print("Writing article")


def run_seo():
    """Perform SEO optimization."""
    print("Running SEO optimization")


def qa_validate():
    """Run quality assurance checks."""
    print("Running QA checks")


def publish_to_wp():
    """Publish the article to WordPress."""
    print("Publishing to WordPress")


STEP_REGISTRY = {
    "keyword_generator": gen_keywords,
    "content_writer": write_article,
    "seo_optimizer": run_seo,
    "qa_checker": qa_validate,
    "publisher": publish_to_wp,
}

PIPELINE_ORDER = [
    "keyword_generator",
    "content_writer",
    "seo_optimizer",
    "qa_checker",
    "publisher",
]

if __name__ == "__main__":
    for step in PIPELINE_ORDER:
        STEP_REGISTRY[step]()
