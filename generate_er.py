
import xml.etree.ElementTree as ET
import uuid

def generate_drawio_xml():
    mxfile = ET.Element('mxfile', host="app.diagrams.net", modified="2024-01-31T00:00:00.000Z", agent="Antigravity", version="23.0.0", type="device")
    diagram = ET.SubElement(mxfile, 'diagram', id="diagram_id", name="ViralPrompt ER Diagram")
    mx_graph_model = ET.SubElement(diagram, 'mxGraphModel', dx="1422", dy="791", grid="1", gridSize="10", guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1", pageWidth="1169", pageHeight="827", math="0", shadow="0")
    root = ET.SubElement(mx_graph_model, 'root')
    
    ET.SubElement(root, 'mxCell', id="0")
    ET.SubElement(root, 'mxCell', id="1", parent="0")

    tables = {
        "users": ["id (PK)", "email", "username", "display_name", "role", "credits_balance", "created_at"],
        "user_followers": ["follower_id (PFK)", "following_id (PFK)", "created_at"],
        "user_settings": ["user_id (PK, FK)", "theme", "language", "notifications"],
        "prompt_categories": ["id (PK)", "name", "slug", "description"],
        "prompts": ["id (PK)", "user_id (FK)", "category_id (FK)", "title", "prompt_text", "type", "like_count"],
        "prompt_tags": ["id (PK)", "name", "slug", "use_count"],
        "prompt_tag_relations": ["prompt_id (PFK)", "tag_id (PFK)"],
        "prompt_likes": ["user_id (PFK)", "prompt_id (PFK)"],
        "prompt_saves": ["user_id (PFK)", "prompt_id (PFK)", "collection_id"],
        "content": ["id (PK)", "user_id (FK)", "prompt_id (FK)", "title", "type", "media_url", "view_count"],
        "content_tags": ["content_id (PFK)", "tag_id (PFK)"],
        "content_likes": ["user_id (PFK)", "content_id (PFK)"],
        "content_views": ["id (PK)", "content_id (FK)", "user_id (FK)", "watch_duration"],
        "comments": ["id (PK)", "content_id (FK)", "user_id (FK)", "parent_id (FK)", "body"],
        "collections": ["id (PK)", "user_id (FK)", "name", "is_public"],
        "collection_items": ["id (PK)", "collection_id (FK)", "content_id (FK)", "prompt_id (FK)"],
        "generation_jobs": ["id (PK)", "user_id (FK)", "type", "status", "result_content_id (FK)"],
        "credit_transactions": ["id (PK)", "user_id (FK)", "amount", "type", "job_id (FK)"],
        "trending_content": ["id (PK)", "content_id (FK)", "period", "score"],
        "trending_hashtags": ["id (PK)", "tag_id (FK)", "period", "mention_count"],
        "user_analytics": ["id (PK)", "user_id (FK)", "date", "views", "likes"],
        "notifications": ["id (PK)", "user_id (FK)", "type", "title", "is_read"]
    }

    relationships = [
        ("user_followers", "users", "follower_id"),
        ("user_followers", "users", "following_id"),
        ("user_settings", "users", "user_id"),
        ("prompts", "users", "user_id"),
        ("prompts", "prompt_categories", "category_id"),
        ("prompt_tag_relations", "prompts", "prompt_id"),
        ("prompt_tag_relations", "prompt_tags", "tag_id"),
        ("prompt_likes", "users", "user_id"),
        ("prompt_likes", "prompts", "prompt_id"),
        ("prompt_saves", "users", "user_id"),
        ("prompt_saves", "prompts", "prompt_id"),
        ("content", "users", "user_id"),
        ("content", "prompts", "prompt_id"),
        ("content_tags", "content", "content_id"),
        ("content_tags", "prompt_tags", "tag_id"),
        ("content_likes", "users", "user_id"),
        ("content_likes", "content", "content_id"),
        ("content_views", "content", "content_id"),
        ("content_views", "users", "user_id"),
        ("comments", "content", "content_id"),
        ("comments", "users", "user_id"),
        ("comments", "comments", "parent_id"),
        ("collections", "users", "user_id"),
        ("collection_items", "collections", "collection_id"),
        ("collection_items", "content", "content_id"),
        ("collection_items", "prompts", "prompt_id"),
        ("generation_jobs", "users", "user_id"),
        ("generation_jobs", "content", "result_content_id"),
        ("credit_transactions", "users", "user_id"),
        ("credit_transactions", "generation_jobs", "job_id"),
        ("trending_content", "content", "content_id"),
        ("trending_hashtags", "prompt_tags", "tag_id"),
        ("user_analytics", "users", "user_id"),
        ("notifications", "users", "user_id")
    ]

    table_ids = {}
    
    # Layout constants
    TABLE_WIDTH = 200
    SPACING_X = 250
    SPACING_Y = 300
    COLS = 5

    for i, (table_name, cols) in enumerate(tables.items()):
        t_id = f"table_{i}"
        table_ids[table_name] = t_id
        
        tx = (i % COLS) * SPACING_X + 20
        ty = (i // COLS) * SPACING_Y + 20
        t_height = 30 + len(cols) * 30
        
        # Table Container
        style = "swimlane;fontStyle=0;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#1a1a1a;strokeColor=#4d4d4d;fontColor=#ffffff;separatorColor=#4d4d4d;"
        mxCell = ET.SubElement(root, 'mxCell', id=t_id, value=table_name, style=style, parent="1", vertex="1")
        # Important: use 'as="geometry"' (not 'as_="geometry"') and ensure all attributes are strings
        mxGeometry = ET.SubElement(mxCell, 'mxGeometry', x=str(tx), y=str(ty), width=str(TABLE_WIDTH), height=str(t_height), as="geometry")
        
        for j, col in enumerate(cols):
            c_id = f"row_{i}_{j}"
            c_style = "text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;fontColor=#ffffff;"
            c_cell = ET.SubElement(root, 'mxCell', id=c_id, value=col, style=c_style, parent=t_id, vertex="1")
            ET.SubElement(c_cell, 'mxGeometry', y=str(30 + j * 30), width=str(TABLE_WIDTH), height="30", as="geometry")

    # Connectors
    for i, (src, dest, field) in enumerate(relationships):
        r_id = f"rel_{i}"
        # Using a more standard edge style
        style = "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#666666;endArrow=ERmany;endFill=0;startArrow=ERone;startFill=0;"
        mxCell = ET.SubElement(root, 'mxCell', id=r_id, value="", style=style, edge="1", parent="1", source=table_ids[src], target=table_ids[dest])
        ET.SubElement(mxCell, 'mxGeometry', relative="1", as="geometry")

    # Convert to string and ensure 'as' attribute is correct (ElementTree might escape it or treat it weirdly if passed as keyword)
    # Actually, ET uses 'as' if passed as 'as'. Let's check the previous output.
    # The previous output had 'as_="geometry"' which is definitely wrong.
    
    return ET.tostring(mxfile, encoding='unicode')

if __name__ == "__main__":
    xml_content = generate_drawio_xml()
    # Correcting the 'as' attribute manually because 'as' is a reserved keyword in Python
    xml_content = xml_content.replace('as_="geometry"', 'as="geometry"')
    
    with open("c:/jmd/preet/antigravity_projects/viral-prompt/docs/er_diagram.drawio", "w", encoding="utf8") as f:
        f.write(xml_content)
