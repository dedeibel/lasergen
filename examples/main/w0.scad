
            difference() {
            
        translate([-4.0, -4.0, 0])
        color("grey")
        linear_extrude(height = 4.0 * 1, center = true, convexity = 10)
        import (file = "w0-outline.dxf");
        
        translate([-4.0, -4.0, 0])
        color("grey")
        linear_extrude(height = 4.0 * 1.1, center = true, convexity = 10)
        import (file = "w0-d0.dxf");
        
        translate([-4.0, -4.0, 0])
        color("grey")
        linear_extrude(height = 4.0 * 1.1, center = true, convexity = 10)
        import (file = "w0-d1.dxf");
        
            } // end difference
            