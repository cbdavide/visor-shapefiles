from mapnik import Style, Rule, Color, PolygonSymbolizer, LineSymbolizer

def basicStyle():
    s = Style()
    r = Rule()

    polygon_symbolizer = PolygonSymbolizer()
    polygon_symbolizer.fill = Color('#f2eff9')
    r.symbols.append(polygon_symbolizer)

    line_symbolizer = LineSymbolizer()
    line_symbolizer.stroke = Color('rgb(50%, 50%, 50%)')
    line_symbolizer.stroke_width = 0.1
    r.symbols.append(line_symbolizer)

    s.rules.append(r)
    return s
