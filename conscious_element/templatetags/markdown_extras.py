import re

import markdown as md
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def markdown(value):
    html = md.markdown(value, extensions=["markdown.extensions.fenced_code"])

    """
    The selected code uses a regular expression to find and replace Mermaid code blocks in the HTML generated from Markdown. 
    
    ``` python
        re.compile(r'<pre><code class="language-mermaid">(.*?)</code></pre>', re.DOTALL)
    ```
    This compiles a regex pattern to match Mermaid code blocks.
    
    <pre><code class="language-mermaid">: Matches the opening tags of a code block with the class language-mermaid.
    
    - (.*?): A non-greedy match for any content inside the code block.
    
    - </code></pre>: Matches the closing tags of the code block.
    
    - re.DOTALL: Allows the . to match newline characters, enabling the pattern to match multi-line content.
    
    ``` python
        html = mermaid_pattern.sub(r'<div class="mermaid">\1</div>', html)
    ```
    This replaces the matched Mermaid code blocks with a div element.
    
    r'<div class="mermaid">\1</div>': The replacement string, where \1 refers to the content captured by the first group (.*?).
    
    html: The input HTML string where the replacement occurs.
    """

    mermaid_pattern = re.compile(r'<pre><code class="language-mermaid">(.*?)</code></pre>', re.DOTALL)
    html = mermaid_pattern.sub(r'<div class="mermaid">\1</div>', html)

    return html
