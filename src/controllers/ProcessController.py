from .BaseController import BaseController
from assets.routes.schemes.data import ProcessDataRequest   
import os  # pyright: ignore[reportMissingImports]
from langchain_community.document_loaders import TextLoader  # pyright: ignore[reportMissingImports]  
from langchain_community.document_loaders import PyMuPDFLoader  # pyright: ignore[reportMissingImports]
from models.enums.ProcessingEnums import ProcessingEnums  # pyright: ignore[reportMissingImports]   
from langchain_text_splitters import RecursiveCharacterTextSplitter  # pyright: ignore[reportMissingImports] 



class ProcessController(BaseController):

    def __init__(self, project_id: str, file_id: str, chunk_size: int, overlap_size: int, do_reset: bool ):
        super().__init__()
        self.project_id = project_id
        self.file_id = file_id
        self.chunk_size = chunk_size
        self.overlap_size = overlap_size
        self.do_reset = do_reset
        self.project__path = ProcessController.get_project_path(project_id)

    def get_file_extension(self, file_name: str) -> str:
        _, file_extension = os.path.splitext(file_name)
        return file_extension

    def get_file_loader(self, file_path: str):
        file_extension = self.get_file_extension(file_path)
        if file_extension == ProcessingEnums.TEXT.value:
            return TextLoader(file_path)    
        elif file_extension == ProcessingEnums.PDF.value:
            return PyMuPDFLoader(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")    


    def get_file_cotent(self, file_path: str):
        loader = self.get_file_loader(file_path)
        documents = loader.load()
        return documents
        

    def process_file_content(self, file_path: str, file_content: list, chunck_size: int=100, overlap_size: int=20):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunck_size, chunk_overlap=overlap_size, length_function=len)

        file_content_texts = [doc.page_content for doc in file_content]
        file_content_metadata = [doc.metadata for doc in file_content]
        chunks = text_splitter.split_documents(file_content)    

        return chunks, file_content_texts, file_content_metadata
       
