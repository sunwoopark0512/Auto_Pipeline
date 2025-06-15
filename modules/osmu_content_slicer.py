def slice_text(text: str, max_len: int = 2200) -> list[str]:
    """
    긴 블로그/기사 원문을 최대 max_len 글자 단위로 잘라
    인스타그램, X(Twitter) 등 소셜 포스트용 슬라이스 리스트 반환
    """
    words = text.split()
    chunks, current = [], []
    for w in words:
        if len(" ".join(current + [w])) > max_len:
            chunks.append(" ".join(current))
            current = [w]
        else:
            current.append(w)
    if current:
        chunks.append(" ".join(current))
    return chunks
