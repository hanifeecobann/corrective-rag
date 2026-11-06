import os
from dotenv import load_dotenv

load_dotenv()
#buradaki key ve value değeri sayesinde web  sitelerinin bizi bot sanmasını engelliyoruz.Windows’ta Hugging Face’in symlink uyarısını susturur.
os.environ.setdefault("USER_AGENT", "CorrectiveRAG")
os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")


#RecursiveCharacterTextSplitter	Uzun metni parçalara böler,
#WebBaseLoader: Belirtilen URL'lerdeki HTML içeriklerini indirip LangChain'in standart Document nesnelerine dönüştürür (metni ve meta verileri -başlık, URL vb.- ayıklar),
#Chroma	Vektör veritabanı,Vektörleri disk üzerindeki bir klasörde (persist_directory) saklar, böylece her çalıştırıldığında verileri yeniden indekslemek zorunda kalmazsın.
#HuggingFaceEmbeddings: Metinleri sayısal vektörlere dönüştürmek için HuggingFace üzerindeki modelleri yerel olarak (CPU veya GPU'da) çalıştırmanı sağlar.
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings



#kaynaklar
urls = [
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    "https://lilianweng.github.io/posts/2026-07-04-harness/",
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
]

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vectorstore = Chroma(
    collection_name="rag_chroma",
    embedding_function=embeddings,
    persist_directory="./.chroma",
)

# Veritabanı boşsa: dokümanları indir, parçala ve indeksle (sadece ilk çalıştırmada)
if vectorstore._collection.count() == 0:
    docs = [WebBaseLoader(url).load() for url in urls]
    docs_list = [item for sublist in docs for item in sublist]  # listeleri tek listeye düzleştirir

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=250, chunk_overlap=0
    )
    splits = text_splitter.split_documents(docs_list)

    batch_size = 100
    for i in range(0, len(splits), batch_size):
        vectorstore.add_documents(splits[i:i + batch_size])
        print(f"{min(i + batch_size, len(splits))}/{len(splits)} parça indekslendi")

retriever = vectorstore.as_retriever()