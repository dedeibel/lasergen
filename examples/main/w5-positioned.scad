
            translate([0.0, 0.0, -2.0])
            rotate([0,0,0]) {
                
            difference() {
            
        translate([-4.0, -4.0, 0])
        color("grey")
        linear_extrude(height = 4.0 * 1, center = true, convexity = 10)
        import (file = "w5-outline.dxf");
        
        translate([-4.0, -4.0, 0])
        color("grey")
        linear_extrude(height = 4.0 * 1.1, center = true, convexity = 10)
        import (file = "w5-d0.dxf");
        
        translate([-4.0, -4.0, 0])
        color("grey")
        linear_extrude(height = 4.0 * 1.1, center = true, convexity = 10)
        import (file = "w5-d1.dxf");
        
        translate([-4.0, -4.0, 0])
        color("grey")
        linear_extrude(height = 4.0 * 1.1, center = true, convexity = 10)
        import (file = "w5-d2.dxf");
        
        translate([-4.0, -4.0, 0])
        color("grey")
        linear_extrude(height = 4.0 * 1.1, center = true, convexity = 10)
        import (file = "w5-d3.dxf");
        
        translate([-4.0, -4.0, 0])
        color("grey")
        linear_extrude(height = 4.0 * 1.1, center = true, convexity = 10)
        import (file = "w5-d4.dxf");
        
        translate([-4.0, -4.0, 0])
        color("grey")
        linear_extrude(height = 4.0 * 1.1, center = true, convexity = 10)
        import (file = "w5-d5.dxf");
        
        translate([-4.0, -4.0, 0])
        color("grey")
        linear_extrude(height = 4.0 * 1.1, center = true, convexity = 10)
        import (file = "w5-d6.dxf");
        
        translate([-4.0, -4.0, 0])
        color("grey")
        linear_extrude(height = 4.0 * 1.1, center = true, convexity = 10)
        import (file = "w5-d7.dxf");
        
            } // end difference
            
            } // end rotate
            