import arxiv
import datetime
from dateutil.relativedelta import relativedelta
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_ml_papers(max_results: int=1000):
    # calculate date 6 months ago
    six_months_ago = datetime.datetime.now() - relativedelta(months=6)

    query = "cat:cs.LG OR cat:cs.AI OR cat:cs.CL OR cat:cs.CV OR cat:stat.ML"


    client = arxiv.Client()
    batch_size = 100
    papers = []

    for start in range(0, max_results, batch_size):
        search = arxiv.Search(
            query=query,
            max_results=batch_size,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending,
            start=start
        )
        batch = list(client.results(search))
        if not batch:
            break  # No more results
        papers.extend(batch)
        if len(batch) < batch_size:
            break  # Last batch


def push_to_db(papers):
    conn = None
    try:
        password = os.environ.get("DB_PASSWORD")
        conn = psycopg2.connect(
            host="127.0.0.1",
            user="postgres",
            password=password,
            dbname="postgres"
        )
        cursor = conn.cursor()
    except Exception as e:
        print(f"Error: {e}")
        return

    for paper in papers:

        title = paper.title.replace("'", "''")
        authors = ', '.join([author.name for author in paper.authors]).replace("'", "''")
        summary = paper.summary.replace("'", "''")
        published = paper.published
        updated = paper.updated
        primary_category = paper.primary_category
        categories = ', '.join(paper.categories)
        pdf_url = paper.pdf_url
        arxiv_id = paper.get_short_id()
        doi = paper.doi if paper.doi else ''
        journal_ref = paper.journal_ref if paper.journal_ref else ''
        comment = paper.comment if paper.comment else ''

        cursor.execute("""
            INSERT INTO papers (arxiv_id, title, authors, summary, published, updated, primary_category, categories, pdf_url, doi, journal_ref, comment)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (arxiv_id) DO NOTHING;
        """,
        (arxiv_id, title, authors, summary, published, updated, primary_category, categories, pdf_url, doi, journal_ref, comment)
        )
        conn.commit()
        print(f"Inserted paper {arxiv_id} into database.")


if __name__ == "__main__":
    papers = get_ml_papers(max_results=1000)
    push_to_db(papers)
