
            translate([0.0, 0.0, 62.0])
            rotate([0,0,0]) {
                
            difference() {
            
        translate([-4.0, -4.0, 0])
        color("grey")
        linear_extrude(height = 4.0 * 1, center = true, convexity = 10)
        import (file = "w4-outline.dxf");
        
        translate([-4.0, -4.0, 0])
        color("grey")
        linear_extrude(height = 4.0 * 1.1, center = true, convexity = 10)
        import (file = "w4-d0.dxf");
        
        translate([-4.0, -4.0, 0])
        color("grey")
        linear_extrude(height = 4.0 * 1.1, center = true, convexity = 10)
        import (file = "w4-d1.dxf");
        
        translate([-4.0, -4.0, 0])
        color("grey")
        linear_extrude(height = 4.0 * 1.1, center = true, convexity = 10)
        import (file = "w4-d2.dxf");
        
        translate([-4.0, -4.0, 0])
        color("grey")
        linear_extrude(height = 4.0 * 1.1, center = true, convexity = 10)
        import (file = "w4-d3.dxf");
        
        translate([-4.0, -4.0, 0])
        color("grey")
        linear_extrude(height = 4.0 * 1.1, center = true, convexity = 10)
        import (file = "w4-d4.dxf");
        
            } // end difference
            
            } // end rotate
            