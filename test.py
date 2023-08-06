from langchain.document_loaders.image import UnstructuredImageLoader
loader = UnstructuredImageLoader("documents/fiche-de-paie.png")
print(loader.load())
