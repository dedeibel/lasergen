
all: export.stl

%.dxf: %.ps
	pstoedit -dt -f dxf:-polyaslines\ -mm $< $@

%.ps: %.svg
	inkscape -C -P $@ $<

%.stl: %.scad
	openscad -o $@ $<

export.stl: w0-positioned.stl w1-positioned.stl w2-positioned.stl w3-positioned.stl w4-positioned.stl w5-positioned.stl w6-positioned.stl


.PHONY: all view

view: w0-positioned.stl w1-positioned.stl w2-positioned.stl w3-positioned.stl w4-positioned.stl w5-positioned.stl w6-positioned.stl
	openscad export.scad &

export.stl:
	cat w0-positioned.stl w1-positioned.stl w2-positioned.stl w3-positioned.stl w4-positioned.stl w5-positioned.stl w6-positioned.stl > export.stl

w0.stl: w0-outline.dxf w0-d0.dxf w0-d1.dxf
view-w0: w0-outline.dxf w0-d0.dxf w0-d1.dxf
	openscad w0.scad &
.PHONY: view-w0
w0-positioned.stl: w0-outline.dxf w0-d0.dxf w0-d1.dxf

w1.stl: w1-outline.dxf w1-d0.dxf w1-d1.dxf
view-w1: w1-outline.dxf w1-d0.dxf w1-d1.dxf
	openscad w1.scad &
.PHONY: view-w1
w1-positioned.stl: w1-outline.dxf w1-d0.dxf w1-d1.dxf

w2.stl: w2-outline.dxf
view-w2: w2-outline.dxf
	openscad w2.scad &
.PHONY: view-w2
w2-positioned.stl: w2-outline.dxf

w3.stl: w3-outline.dxf
view-w3: w3-outline.dxf
	openscad w3.scad &
.PHONY: view-w3
w3-positioned.stl: w3-outline.dxf

w4.stl: w4-outline.dxf w4-d0.dxf w4-d1.dxf w4-d2.dxf w4-d3.dxf w4-d4.dxf
view-w4: w4-outline.dxf w4-d0.dxf w4-d1.dxf w4-d2.dxf w4-d3.dxf w4-d4.dxf
	openscad w4.scad &
.PHONY: view-w4
w4-positioned.stl: w4-outline.dxf w4-d0.dxf w4-d1.dxf w4-d2.dxf w4-d3.dxf w4-d4.dxf

w5.stl: w5-outline.dxf w5-d0.dxf w5-d1.dxf w5-d2.dxf w5-d3.dxf w5-d4.dxf w5-d5.dxf w5-d6.dxf w5-d7.dxf
view-w5: w5-outline.dxf w5-d0.dxf w5-d1.dxf w5-d2.dxf w5-d3.dxf w5-d4.dxf w5-d5.dxf w5-d6.dxf w5-d7.dxf
	openscad w5.scad &
.PHONY: view-w5
w5-positioned.stl: w5-outline.dxf w5-d0.dxf w5-d1.dxf w5-d2.dxf w5-d3.dxf w5-d4.dxf w5-d5.dxf w5-d6.dxf w5-d7.dxf

w6.stl: w6-outline.dxf
view-w6: w6-outline.dxf
	openscad w6.scad &
.PHONY: view-w6
w6-positioned.stl: w6-outline.dxf
