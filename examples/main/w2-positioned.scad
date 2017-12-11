
            translate([0.0, 122.0, 0.0])
            rotate([90,0,0]) {
                
        translate([-4.0, -4.0, 0])
        color("grey")
        linear_extrude(height = 4.0 * 1, center = true, convexity = 10)
        import (file = "w2-outline.dxf");
        
            } // end rotate
            