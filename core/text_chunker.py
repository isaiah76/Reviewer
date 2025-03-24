from config.settings import MAX_CHUNK_SIZE

def chunk_text(text, max_chunk_size=MAX_CHUNK_SIZE):
    """Split text into chunks if it exceeds the maximum size of the context window."""
    if len(text) <= max_chunk_size:
        return [text]
    
    chunks = []
    current_pos = 0
    while current_pos < len(text):
        # find a good breaking point
        end_pos = min(current_pos + max_chunk_size, len(text))
        if end_pos < len(text):
            # find a paragraph break
            paragraph_break = text.rfind('\n\n', current_pos, end_pos)
            if paragraph_break != -1 and paragraph_break > current_pos + max_chunk_size // 2:
                end_pos = paragraph_break + 2
            else:
                # If no good paragraph break try a sentence break
                sentence_break = text.rfind('. ', current_pos, end_pos)
                if sentence_break != -1 and sentence_break > current_pos + max_chunk_size // 2:
                    end_pos = sentence_break + 2
        
        chunks.append(text[current_pos:end_pos])
        current_pos = end_pos
    
    return chunks
