from ..GraphqlClient.GraphQLClient import GraphQLClient
from Giveme5W1H.extractor.document import Document
from Giveme5W1H.extractor.extractor import MasterExtractor  
import logging
import time
    

class Giveme5W1HUpdator():
    _client = None
    _giveme5WExtractor = None 
    _cursor = None
    _fetchSize = 100

    def __init__(self):
        if (GraphQLClient is None):
            exit("GraphQLClient was not provided to the Giveme5W1HUpdator")

        self._client = GraphQLClient()
        self._giveme5WExtractor = MasterExtractor()

    def summariseArticles(self):
        # Grab content in batches (via pagination) to make it more managable
        loopCounter = 0
        totalArticlesSummarised = 0
        startTime = time.time()

        print(f"Init summarising loop with fetchSize={self._fetchSize}...")
        while True:
            print(f"Entering loop number: {loopCounter}")
            print("Fetching articles...")
            edges = self.fetchArticles()

            if (edges is None):
                print("No more content found to summarise")
                break

            for edge in edges:
                node = edge['node']
                summary = self.summariseContent(node)
                self.updateDatabaseWithTextSummary(node['id'], summary)
                summary.clear()
                
                # update the graphQL cursor 
                self._cursor = edge['cursor']

            loopCounter += 1

        totalTime = time.time() - startTime
        print(f"Summarised {totalArticlesSummarised} in {totalTime} seconds. Averaged {float(totalArticlesSummarised)/totalTime} articles per second")

    # Fetch article content from graphQL API
    def fetchArticles(self):
        # parameters for query
        params = {
            "fetchSize": self._fetchSize,
            "cursor": self._cursor
        }

        returnedJson = self._client.executeQuery(self.allArticlesGQL(), params)
        edges = returnedJson["allArticles"]["edges"]
        print(f"Successfully fetched {len(edges)} articles.")
        return edges

    # Given content, return a summarised version 
    def summariseContent(self, node):
        content = node['articlecontentByContentId']['content']
        publicationDate = node['publicationDate']
        title = node['title']
        doc = Document(title=title, desc='', text=content, date=publicationDate)

        # Parse content - sends request to the server
        doc = self._giveme5WExtractor.parse(doc)

        # Retrieved parsed information
        summary = {
            'who': None,
            'what': None, 
            'when': None,
            'where': None,
            'why': None,
            'how': None
        }

        for key in summary.keys():
            try:
                summary[key] = doc.get_top_answer(key).get_parts_as_text()
            except Exception as e:
                print(f"Text summary - failed to grab answer for {key} - Exception: {e}")
                continue

        return summary


    def updateDatabaseWithTextSummary(self, articleId, summary):
        # create the record containing the summary information
        params = {
            "who": summary['who'],
            "what": summary['what'],
            "when": summary['when'],
            "where": summary['where'],
            "how": summary['how'],
            "why": summary['why'] 
        }

        returnedJson = self._client.executeQuery(self.createTextSummaryGQL(), params)
        summaryId = returnedJson['createArticlesummary']['articlesummary']['id']
        print(f"Created the text summary id: {summaryId}")

        # update the existing article record to point to the text summary
        params = {
            "articleId": articleId,
            "textSummaryId": summaryId
        }

        try:
            returnedJson = self._client.executeQuery(self.updateArticleWithTextSummaryGQL(), params)
        except Exception as e:
            print(f"Failed to update article ({articleId}) with textSummaryId({summaryId})")

        
    # GraphQL mutation to push a text summary
    def createTextSummaryGQL(self):
        return """
            mutation CreateSummary($who: String, $what: String, $when: String, $where: String, $how: String, $why: String) {
                createArticlesummary(input: {
                    articlesummary: {
                        who: $who,
                        what: $what,
                        when_: $when,
                        where_: $where,
                        why: $why,
                        how: $how
                    }
                }) {
                    articlesummary {
                        id
                    }
                }
            }
        """

    # GraphQL mutation to update articles with a reference to its text summary
    def updateArticleWithTextSummaryGQL(self):
        return """
            mutation UpdateArticleWithTextSummary($articleId: Int!, $textSummaryId: Int!) {
                updateArticleById(input: {
                    id: $articleId,
                    articlePatch: {
                        textSummaryId: $textSummaryId
                    }
                }) {
                    article {
                        id
                        textSummaryId
                    }
                }
            }
        """

    # Graph QL query to grab articles
    def allArticlesGQL(self):
        return  """
            query FetchArticles($fetchSize: Int = 10, $cursor: Cursor) {
                allArticles(filter: {
                    textSummaryId: {
                        isNull: true
                    }
                }, first: $fetchSize, after: $cursor) {
                    edges {
                        cursor
                        node {
                            id
                            title
                            publicationDate
                            articlecontentByContentId {
                                content
                            }
                        }
                    }
                }
            }
        """
        


