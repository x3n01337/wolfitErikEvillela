import click
from datetime import datetime, timedelta
from random import randint, choice, random
from flask import Blueprint

sample_data = Blueprint("sample_data", __name__)

TITLES = [
    "How do I get started with {}?",
    "Best resources for learning {}",
    "What's your favorite thing about {}?",
    "I built my first {} project!",
    "Tips for debugging in {}",
    "Why does everyone recommend {}?",
    "Struggling with {} - any advice?",
    "Just discovered {} and I'm hooked",
    "{} vs other options - thoughts?",
    "Common mistakes when learning {}",
    "How long did it take you to learn {}?",
    "Weekly {} discussion thread",
    "Is {} good for beginners?",
    "Share your {} project here",
    "What IDE do you use for {}?",
    "Help with a {} error",
    "Finally understanding {} after weeks of practice",
    "What got you interested in {}?",
    "Recommended books for {}?",
    "How do you stay motivated learning {}?",
]

BODIES = [
    "I've been working on this for a while and wanted to share my experience. "
    "It's been a great journey so far and I've learned a lot along the way. "
    "Would love to hear what others think about this topic.",

    "Hey everyone, I'm new here and just getting started. "
    "I've read through some of the beginner guides but I still have questions. "
    "Any tips for someone just starting out would be really appreciated!",

    "After spending a few months on this, I think I finally have a handle on "
    "the basics. The hardest part was understanding how everything fits together. "
    "Once that clicked, things got a lot easier.",

    "I wanted to share a quick tip that helped me a lot: break the problem down "
    "into smaller pieces and tackle each one individually. It sounds obvious but "
    "it really makes a difference when you're feeling overwhelmed.",

    "Does anyone have recommendations for good tutorials or courses? "
    "I've tried a few but they either move too fast or assume too much "
    "prior knowledge. Looking for something aimed at intermediate learners.",

    "Just finished a small project and I'm pretty happy with how it turned out. "
    "It's nothing fancy but it works and I learned a ton in the process. "
    "Planning to add more features over the next few weeks.",

    "I keep running into the same issue and I'm not sure what I'm doing wrong. "
    "I've checked the documentation and searched online but can't find a clear "
    "answer. Has anyone else dealt with this?",

    "One thing I wish I had known earlier is how important it is to read other "
    "people's code. You pick up so many useful patterns and techniques that "
    "you wouldn't discover on your own.",

    "I'm working on a side project and could use some feedback. "
    "It's still a work in progress but I'd love to get some early opinions "
    "on the approach I'm taking.",

    "Thanks to everyone in this community for being so helpful. "
    "I've learned more here in a few weeks than I did in months on my own. "
    "This is a really great place for beginners.",
]

LINK_URLS = [
    "https://example.com/tutorial-getting-started",
    "https://example.com/best-practices-guide",
    "https://example.com/interesting-article",
    "https://example.com/video-walkthrough",
    "https://example.com/open-source-project",
]


@sample_data.cli.command("load")
@click.option("-s", "--subreddit", default="learnpython")
@click.option("-n", "--count", default=100, help="Number of posts to generate")
def load(subreddit, count):
    """Loads randomly generated sample data for the specified subreddit."""
    from app import db
    from app.models import Post

    print(f"Generating sample data for: {subreddit}")

    u = create_user(db, subreddit)
    print(f"Created user: {u.username}")
    c = create_category(db, subreddit)

    now = datetime.utcnow()
    for i in range(count):
        title = choice(TITLES).format(subreddit)
        # Append a number to ensure unique titles
        title = f"{title} (#{i + 1})"

        existing = Post.query.filter_by(title=title).first()
        if existing is not None:
            continue

        # ~20% of posts are link posts
        link = random() < 0.2
        url = choice(LINK_URLS) if link else None
        body = "" if link else choice(BODIES)

        timestamp = now - timedelta(
            days=randint(0, 30),
            hours=randint(0, 23),
            minutes=randint(0, 59),
        )

        p = Post(
            title=title,
            body=body,
            timestamp=timestamp,
            vote_count=randint(0, 500),
            link=link,
            url=url,
            user_id=u.id,
            category_id=c.id,
        )
        print(f"Creating post: {p} in {c.title}")
        db.session.add(p)
        db.session.commit()


def create_user(db, subreddit):
    from app.models import User

    username = f"{subreddit}-{randint(0, 999999)}"
    u = User(username=username, email=f"{username}@example.com")
    u.set_password("wolfit")
    db.session.add(u)
    db.session.commit()
    return u


def create_category(db, subreddit):
    from app.models import Category

    category = None
    category = Category.query.filter_by(title=subreddit).first()
    if category is None:
        category = Category(title=subreddit)
        db.session.add(category)
        db.session.commit()
    return category
