//
// Created by pedro on 12/06/2021.
//

#include "Genes_helpers.h"

namespace Genes_helpers {

    void mutation(boost::dynamic_bitset<> &a, uint rate){
        for (boost::dynamic_bitset<>::size_type i = 0, size = a.size(); i < size; ++i) {
            a[i] ^= (rand()%100001 < rate);
        }
    }

    template<class T>
    void mutationV02(boost::dynamic_bitset<> &a, uint rate){
        /*Mutation on range of objects*/
        const std::size_t object_size = sizeof(T)*8;
        boost::dynamic_bitset<>::size_type number_of_objects = a.size()/object_size;

        for (boost::dynamic_bitset<>::size_type i = object_size*(rand()%number_of_objects),
                last = i + object_size*(1+rand()%(number_of_objects - i/object_size)); i < last; ++i) {
            a[i] ^= (rand()%100001 < rate);
        }
    }
    template void mutationV02<bit_parser_l1>(boost::dynamic_bitset<> &a, uint rate);
    template void mutationV02<bit_parser_l3>(boost::dynamic_bitset<> &a, uint rate);

    State Convert_Bits( bit_parser_l3 *bits ){
        State value;
        value.Position[0] = bits->Position_2[0]%10001 + (bits->Position_2[1]%10000)/10000.0f;
        value.Position[1] = bits->Position_2[2]%10001 + (bits->Position_2[3]%10000)/10000.0f;
        value.angle = (bits->angle % 18001)/100.0f;

        return value;
    }

    State Convert_Bits( bit_parser_l1 *bits ){
        State value;
        uint val = bits->value;
        value.Position[0] = ((val&16383)%10000)/10.0f;//14bits
        val = val >> 14;
        value.Position[1] = ((val&16383)%10000)/10.0f;
        val = val >> 14;//now last 4 bits
        value.angle = val*12;

        return value;
    }

    State Convert_Bits_V02( bit_parser_l1 *bits, CGAL_helpers::Rect_info *rect ){
        State value;
        uint val = bits->value;
        value.Position[0] = (((val&16383)%10000)/10000.0f)*(rect->x_max);//14bits
        val = val >> 14;
        value.Position[1] = (((val&16383)%10000)/10000.0f)*(rect->y_max);
        val = val >> 14;//now last 4 bits
        value.angle = val*12;

        return value;
    }

    void cross(boost::dynamic_bitset<> &a, boost::dynamic_bitset<> &b){
        boost::dynamic_bitset<>::size_type size = a.size();
        boost::dynamic_bitset<>::size_type begin = rand()%(size - 1);
        boost::dynamic_bitset<>::size_type end = begin + rand()%(size - begin) + 1;
        bool aux;
        for (boost::dynamic_bitset<>::size_type i = begin; i < end; ++i) {
            aux = a[i];
            a[i] = b[i];
            b[i] = aux;
        }
    }

    template<class T>
    void crossV02(boost::dynamic_bitset<> &a, boost::dynamic_bitset<> &b){
        const std::size_t object_size = sizeof(T)*8;
        boost::dynamic_bitset<>::size_type number_objects = a.size()/object_size;
        boost::dynamic_bitset<>::size_type begin = object_size*(rand()%number_objects);
        boost::dynamic_bitset<>::size_type end = begin + object_size*(1+rand()%(number_objects - begin/object_size));
        bool aux;
        for (boost::dynamic_bitset<>::size_type i = begin; i < end; ++i) {
            aux = a[i];
            a[i] = b[i];
            b[i] = aux;
        }
    }

    template void crossV02<bit_parser_l1>(boost::dynamic_bitset<> &a, boost::dynamic_bitset<> &b);
    template void crossV02<bit_parser_l3>(boost::dynamic_bitset<> &a, boost::dynamic_bitset<> &b);

    template void convert_genes<bit_parser_l1>(boost::dynamic_bitset<> &genes, std::vector<State> &Values);
    template void convert_genes<bit_parser_l3>(boost::dynamic_bitset<> &genes, std::vector<State> &Values);


    template void convert_genes_V02<bit_parser_l1>(boost::dynamic_bitset<> &genes, std::vector<State> &Values, CGAL_helpers::Rect_info *rect);

}