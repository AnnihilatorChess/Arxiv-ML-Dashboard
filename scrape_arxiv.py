import arxiv
import datetime
from dateutil.relativedelta import relativedelta


def get_ml_papers():
    # calculate date 6 months ago
    six_months_ago = datetime.datetime.now() - relativedelta(months=6)

    query = "cat:cs.LG OR cat:cs.AI OR cat:cs.CL OR cat:cs.CV OR cat:stat.ML"


    client = arxiv.Client()

    search = arxiv.Search(
        query=query,
        max_results=1000,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending
    )

    papers = []
    for result in client.results(search):
        if result.published.replace(t)
