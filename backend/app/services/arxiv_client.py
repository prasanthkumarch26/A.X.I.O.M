import httpx
import asyncio
import xml.etree.ElementTree as ET

class ArxivClient:
    def __init__(self):
        self.client = httpx.AsyncClient(follow_redirects=True)
    
    def _parse_xml(self, xml_data : str):
        root = ET.fromstring(xml_data)
        entries = []
        for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
            entry_dict = {
                "id": entry.find("{http://www.w3.org/2005/Atom}id").text,
                "title": entry.find("{http://www.w3.org/2005/Atom}title").text,
                "authors": [author.find("{http://www.w3.org/2005/Atom}name").text for author in entry.findall("{http://www.w3.org/2005/Atom}author")],
                "summary": entry.find("{http://www.w3.org/2005/Atom}summary").text,
                "published": entry.find("{http://www.w3.org/2005/Atom}published").text,
                "updated": entry.find("{http://www.w3.org/2005/Atom}updated").text,
                "link": entry.find("{http://www.w3.org/2005/Atom}link").get("href"),
                "pdf_link": entry.find("{http://www.w3.org/2005/Atom}link").get("href").replace("abs", "pdf")
            }
            entries.append(entry_dict)
        return entries
    
    async def search(self, query : str, max_results : int = 2):
        response = await self.client.get(f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={max_results}")
        return self._parse_xml(response.text)
    
    async def close(self):
        await self.client.aclose()

async def main():
    client = ArxivClient()
    res = await client.search("transformers")
    print(res)
    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
