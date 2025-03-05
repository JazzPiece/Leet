import requests

def fetch_leetcode_titles():
    """Fetch all LeetCode problem titles (unofficial approach) using problemsetQuestionListV2."""
    graphql_url = "https://leetcode.com/graphql"

    # Updated GraphQL query using problemsetQuestionListV2
    # The 'questions' array includes each problem's 'frontendQuestionId', 'title', etc.
    query = """
    query problemsetQuestionListV2($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
      problemsetQuestionListV2(
        categorySlug: $categorySlug,
        limit: $limit,
        skip: $skip,
        filters: $filters
      ) {
        total
        hasMore
        questions {
          difficulty
          freqBar
          frontendQuestionId
          isFavor
          paidOnly
          status
          title
          titleCn
          titleSlug
          topicTags {
            name
            id
            slug
          }
        }
      }
    }
    """

    all_titles = []
    skip = 0
    limit = 100  # how many problems to fetch per query
    has_more = True

    while has_more:
        variables = {
            "categorySlug": "all",
            "skip": skip,
            "limit": limit,
            "filters": {}
        }

        # Send the POST request
        response = requests.post(graphql_url, json={"query": query, "variables": variables})
        data = response.json()

        # Check if there's an error in the response
        if "data" not in data:
            print("Error: 'data' key not in response. Possibly an error or a need to authenticate.")
            # You can print(data) or data.get("errors") for more details.
            break

        problemset_data = data["data"]["problemsetQuestionListV2"]
        questions = problemset_data["questions"]
        for q in questions:
            # q["frontendQuestionId"] is the problem number, q["title"] is the name.
            # e.g., "1. Two Sum"
            front_id = q["frontendQuestionId"]   # e.g. "1"
            title = q["title"]                   # e.g. "Two Sum"
            all_titles.append(f"{front_id}. {title}")

        has_more = problemset_data["hasMore"]
        skip += limit

        print(f"Fetched {len(all_titles)} so far...")

    return all_titles

def write_titles_to_file(titles, filename="All_LeetCode_Titles.txt"):
    """Write all titles to a text file, one per line."""
    with open(filename, "w", encoding="utf-8") as f:
        for title in titles:
            f.write(title + "\n")

if __name__ == "__main__":
    titles = fetch_leetcode_titles()
    if titles:
        write_titles_to_file(titles, "All_LeetCode_Titles.txt")
        print(f"\nWrote {len(titles)} LeetCode problem titles to 'All_LeetCode_Titles.txt'")
    else:
        print("No titles fetched. Possibly due to an error or need for authentication.")
