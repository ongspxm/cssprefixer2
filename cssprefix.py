import rules

def getStyles(content):
    styles = []
    
    content = content.split('{')
    for i in range(len(content)):
        name = content[i].split('}')[-1].strip()
        if not name: continue
        
        style = content[i+1].split('}')[0].strip()
        rules = []
        for rule in style.split(';'):
            if not rule.count(':'):continue
            rule = map(lambda x:x.strip(), rule.split(':'))
            rules.append([rule[0], ':'.join(rule[1:])])

        styles.append(dict(
            name = name,
            rules = rules 
        ))

    return styles

def generateText(css, minify=False):
    text = []
    for block in css:
        text.append('%s{'%block['name'])

        for rule in block['rules']:
            fmt = '    %s: %s;'
            if minify: 
                fmt = '%s:%s;'
                rule[1] = ','.join(map(lambda x:x.strip(), rule[1].split(',')))
            text.append(fmt%tuple(rule))
        
        if minify: text.append('}')
        else: text.append('}\n')
    
    if minify:
        return ''.join(text)
    else:
        return '\n'.join(text).strip()

def process(content, minify=False):
    css = getStyles(content)
    css2 = []
    for block in css:
        rules2 = []
        for rule in block['rules']:
            rules2 += rules.process(rule)
        block['rules'] = rules2
        css2.append(block)
	
    return generateText(css2, minify)
