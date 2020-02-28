import wikipedia
print (wikipedia.summary("Wikipedia"))

wikipedia.search("Barack")
ny = wikipedia.page("New York")
ny.title
ny.url
ny.content
ny.links[0]
