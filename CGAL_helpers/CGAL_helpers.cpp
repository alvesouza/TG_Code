//
// Created by pedro on 06/06/2021.
//

#include "CGAL_helpers.h"

namespace CGAL_helpers{
    inline float angle_radian( const Vector_2 &v, const Vector_2 &u ){
        Vector_2 v_new = v/sqrt(v.squared_length());
        Vector_2 u_new = u/sqrt(u.squared_length());

        kernel_type dot = v_new*u_new;
        kernel_type cross = v_new[0]*u_new[1] - v_new[1]*u_new[0];
        float t;
        if ( dot != 0 ){
            t = atan(cross/dot);
        }else if( cross > 0){
            t = CGAL_PI;
        } else{
            t = -CGAL_PI;
        }

        return (t > 0)?t:(CGAL_PI + t);//acos(v_new * u_new)*(v_new[1] < u_new[1]?1:-1);//acos(v_new * u_new)/CGAL_PI*180*(v_new[1] < u_new[1]?1:-1);
    }
    inline float angle( const Vector_2 &v, const Vector_2 &u ){
        return angle_radian(v, u)*180/CGAL_PI;
    }
    void Rotate_Polygon_radian(Polygon_2 &p, const float angle){
        Transformation rotate(CGAL::ROTATION, sin(angle), cos(angle));
        std::size_t size = p.size();
        //Point_2 begin = Point_2( p[0].x(), p[0].y() );
        for( std::size_t i = 0; i < size; i++ ){
            p[i] = rotate( p[i] );
        }
    }

    kernel_type Polygons_Area( std::vector<Polygon_2> &polygons ){
        kernel_type area = 0, area_aux;

        for ( ssize_t i = 0, size = polygons.size() ; i < size; ++i) {
            if( polygons[i].area() < 0 )
                area -= polygons[i].area();
            else
                area += polygons[i].area();
        }

        return area;
    }

    void Rotate_Polygon_degree(Polygon_2 &p, const float angle){
        Rotate_Polygon_radian(p, angle*180/CGAL_PI);
    }

    void Translate_Polygon( Polygon_2 &p, const Vector_2 Movement){
        std::size_t size = p.size();
        Point_2 begin = Point_2( p[0].x(), p[0].y() );
        for( std::size_t i = 0; i < size; i++ ){
            p[i] = Point_2( p[i].x() + Movement.x(), p[i].y() + Movement.y() );
        }
    }

    inline kernel_type check_intesection_seg( Polygon_2 &p1, Polygon_2 &p2 ){
        Segment_2 seg01, seg02;
        kernel_type intersections = 0;
        for (std::size_t i = 0, size_01 = p1.size(); i < size_01; i++){
            if ( i +1 < size_01 )
                seg01 = Segment_2(p1[i], p1[i+1]);
            else
                seg01 = Segment_2(p1[i], p1[0]);

            for (std::size_t j = 0, size_02 = p2.size(); j < size_02; j++){
                if ( j +1 < size_02 )
                    seg02 = Segment_2(p2[j], p2[j+1]);
                else
                    seg02 = Segment_2(p2[j], p2[0]);

                intersections += CGAL::do_intersect(seg01, seg02);
            }
        }

        return intersections;
    }
    kernel_type check_intesection( Polygon_2 &p1, Polygon_2 &p2 ){
        kernel_type intersections = check_intesection_seg(p1, p2);

        if( intersections == 0 )
            switch (CGAL::bounded_side_2(p1.begin(), p1.end(), p2[0])) {
                case CGAL::ON_BOUNDED_SIDE:
                case CGAL::ON_BOUNDARY:
                    return p1.size()*p2.size();
            }

        if ( intersections == 0 )
            switch (CGAL::bounded_side_2(p2.begin(), p2.end(), p1[0])) {
                case CGAL::ON_BOUNDED_SIDE:
                case CGAL::ON_BOUNDARY:
                    return p1.size()*p2.size();
            }
        return intersections;
    }

    kernel_type check_intesection_inside( Polygon_2 &p1, Polygon_2 &p2 ){
        kernel_type intersections = check_intesection_seg(p1, p2);

        if( intersections == 0 )
            switch (CGAL::bounded_side_2(p1.begin(), p1.end(), p2[0])) {
                case CGAL::ON_UNBOUNDED_SIDE:
                case CGAL::ON_BOUNDARY:
                    return p1.size()*p2.size();
            }

        if ( intersections == 0 )
            switch (CGAL::bounded_side_2(p2.begin(), p2.end(), p1[0])) {
                case CGAL::ON_UNBOUNDED_SIDE:
                case CGAL::ON_BOUNDARY:
                    return p1.size()*p2.size();
            }

        return intersections;
    }

    kernel_type Calculate_Intersection_Area( Polygon_2 &p1, Polygon_2 &p2 ){
        //std::list<Polygon_with_holes_2> polyI;
        //CGAL::intersection( p1, p2, std::back_inserter(polyI));
        kernel_type a = check_intesection(p1, p2);
        //kernel_type totalArea = 0;
        /*for(std::list<Polygon_with_holes_2>::iterator lit = polyI.begin(); lit != polyI.end(); ++lit)
        {
            totalArea += lit->outer_boundary().area();
        }*/
        //std::cout << "totalArea = " << totalArea << std::endl;
        //return totalArea;
        return a;
    }

    Polygon_2 Get_Convex_Hull( std::vector<Point_2> &points ){
        std::vector<std::size_t> indices(points.size()), out;
        std::iota(indices.begin(), indices.end(),0);
        CGAL::convex_hull_2(indices.begin(), indices.end(), std::back_inserter(out),
                            Convex_hull_traits_2(CGAL::make_property_map(points)));

        Polygon_2 hull;

        for (std::size_t i: out) {
            hull.push_back( points[ i ] );
        }

        return hull;
    }

    kernel_type All_Intersection_Area( std::vector<Polygon_2> &polygons ){
        kernel_type all_area = 0;
        for (std::size_t i = 0, size = polygons.size(); i < size; ++i) {
            for (std::size_t j = i + 1; j < size; ++j) {
                all_area += Calculate_Intersection_Area( polygons[i], polygons[j] );
            }
        }

        return all_area;
    }

    kernel_type All_Intersection_Inside_Board_Area( std::vector<Polygon_2> &polygons, Polygon_2 &board ){
        kernel_type all_area = 0;
        for (std::size_t i = 0, size = polygons.size(); i < size; ++i) {
            all_area += check_intesection_inside( polygons[i], board );
        }

        return all_area;

    }

    kernel_type Min_Rect_XY_Area( std::vector<Polygon_2> &polygons ){
        kernel_type x_min = polygons[0][0].x(),x_max = polygons[0][0].x();
        kernel_type y_min = polygons[0][0].y(), y_max = polygons[0][0].y();
        kernel_type x,y;
        for (std::size_t i = 0, size_vector = polygons.size(); i < size_vector; ++i) {
            for (std::size_t j = 0, size_poly = polygons[i].size(); j < size_poly; ++j){
                x = polygons[i][j].x();
                y = polygons[i][j].y();

                if ( x > x_max)
                    x_max = x;
                else if ( x < x_min )
                    x_min = x;

                if ( y > y_max)
                    y_max = y;
                else if ( y < y_min )
                    y_min = y;
            }
        }
        return ( x_max - x_min )*( y_max - y_min );
    }
    kernel_type Min_Rect_XY_Area_V01( std::vector<Polygon_2> &polygons ){
        kernel_type x_max = polygons[0][0].x();
        kernel_type y_max = polygons[0][0].y();
        kernel_type x,y;
        for (std::size_t i = 0, size_vector = polygons.size(); i < size_vector; ++i) {
            for (std::size_t j = 0, size_poly = polygons[i].size(); j < size_poly; ++j){
                x = polygons[i][j].x();
                y = polygons[i][j].y();

                if ( x > x_max)
                    x_max = x;
                else if (x < 0)
                    return 9999999999;

                if ( y > y_max)
                    y_max = y;
                else if (y < 0)
                    return 9999999999;
            }
        }
        return x_max*y_max;
    }


    Rect_info Min_Rect_XY_Area_V02( std::vector<Polygon_2> &polygons ){
        kernel_type x_max = polygons[0][0].x(), x_min = x_max;
        kernel_type y_max = polygons[0][0].y(), y_min = y_max;
        kernel_type x,y;
        for (std::size_t i = 0, size_vector = polygons.size(); i < size_vector; ++i) {
            for (std::size_t j = 0, size_poly = polygons[i].size(); j < size_poly; ++j){
                x = polygons[i][j].x();
                y = polygons[i][j].y();

                if ( x > x_max)
                    x_max = x;
                else if( x < x_min )
                    x_min = x;
                if ( y > y_max)
                    y_max = y;
                else if( y < y_min )
                    y_min = y;
            }
        }

       return {x_max - x_min, y_max - y_min, (x_max - x_min)*(y_max - y_min)};
    }

}
