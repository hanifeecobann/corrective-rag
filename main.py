

from dotenv import load_dotenv
load_dotenv()
from graph.graph import app



if __name__ == '__main__':
    result = app.invoke(input={"question": "agent memory ne?"})
    print("\n=== SONUÇ ===")
    print(result["generation"])

