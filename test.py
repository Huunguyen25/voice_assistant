import wikipedia
import wikipediaapi

def get_summary(query, sentence_limit=2):
    try:
        # Create a Wikipedia object for the English language
        wiki_wiki = wikipediaapi.Wikipedia('voiceassistant', 'en')

        # Refine the input query
        refined_query = query.lower().replace("who is", "").replace("what is", "").strip()

        # Perform the search using the wikipedia module
        search_results = wikipedia.search(refined_query)

        if not search_results:
            print(f"No Wikipedia pages found for '{refined_query}'. Please try another search.")
            return

        # Filter out too general matches, and pick the most relevant page
        best_match = None
        for result in search_results:
            # Check for more specific results (avoid pages that are too broad)
            if len(result.split()) > 1:  # This avoids overly general matches like "PC"
                best_match = result
                break

        if not best_match:
            # If no valid match is found, fall back to the first search result
            best_match = search_results[0]

        print(f"Using the best match: {best_match}")

        # Perform the actual page lookup using wikipediaapi
        page = wiki_wiki.page(best_match)

        # Check if the page exists
        if not page.exists():
            print(f"No Wikipedia page found for '{best_match}'. Please try another search.")
            return

        # Split the summary into sentences and limit to `sentence_limit` sentences
        summary_sentences = page.summary.split('.')
        limited_summary = '. '.join(summary_sentences[:sentence_limit]) + '.' if sentence_limit > 0 else ''

        # Check if the summary is too short or not meaningful
        if len(limited_summary.split()) < 5:
            print(f"Summary for {page.title}: The summary is too short to provide useful information.")
        else:
            print(f"Summary for {page.title}:")
            print(limited_summary)

    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    user_input = input("Search result: ")
    get_summary(user_input, sentence_limit=2)
