
QUERY = """query ScenarioStartViewGetScenario($shortId: String, $viewPublished: Boolean) {
  scenario(shortId: $shortId, viewPublished: $viewPublished) {
    title
    description
    image
    storyCardCount
    tags
    nsfw
    contentRating
    type
    state(viewPublished: $viewPublished) {
      prompt
      plotEssentials
      authorsNote
      __typename
    }
  }
}"""

