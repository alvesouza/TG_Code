TG01_CodePATH = '/home/pedro/Documents/gits/github/TG01_Code'
import sys
from math import acos, pi
sys.path.append(TG01_CodePATH)
import TG01_Code
def makeRotatingPlacement(axis_origin, axis_dir, angle):
    #import FreeCAD as App
    OZ = App.Vector(0,0,1)
    local_cs = App.Placement(axis_origin, App.Rotation(OZ, axis_dir))
    return local_cs.multiply(   App.Placement( App.Vector(), App.Rotation(angle,0,0) ).multiply( local_cs.inverse() )   )

def Rotate2ShorterstHeight( objs ):
    for obj in objs:
        #print('\n////////////////////////////////////////\nlabel is {0}'.format(q))
        if 'Shape' in dir(obj):
            if str(type(obj)) == "<class 'PartDesign.Body'>":
                s = obj.Shape
                p = obj.Placement
                b = p.Base
                r = p.Rotation
                faces = s.Faces
                #print(dir(faces[0]))
                size_list = len(faces)
                best_face = -1
                smallest_height = 9999999
                for i in range( size_list ):
                    height = -1
                    for j in range( size_list ):
                        if i == j:
                            continue
                        for vertex in faces[j].Vertexes:
                            distance = faces[i].distToShape( vertex )[0]
                            if height < distance:
                                height = distance
                    #print( "height = ", height )
                    if height < smallest_height:
                        smallest_height = height
                        best_face = i

                print( "best_face = {0}, smallest_height = {1}".format(best_face, smallest_height) )
                uv = faces[ best_face ].Surface.parameter(faces[ best_face ].CenterOfMass)
                faceNormalInCOM = faces[ best_face ].normalAt(uv[0], uv[1])
                #print("dir face = {0}".format( dir( faces[ best_face ] )))
                print( "Faces Normal = {0}".format(faceNormalInCOM) )
                center_mass = faces[best_face].CenterOfMass
                angle = acos( -faceNormalInCOM[2] )*180/(pi)
                spin = makeRotatingPlacement(App.Vector(b[0], b[1], b[2]), App.Vector(-faceNormalInCOM[1], faceNormalInCOM[0], 0), angle)
                obj.Placement = spin.multiply(obj.Placement)

def LowestHeightOnZero( objs ):
    for obj in objs:
        #print('\n////////////////////////////////////////\nlabel is {0}'.format(q))
        if 'Shape' in dir(obj):
            if str(type(obj)) == "<class 'PartDesign.Body'>":
                s = obj.Shape
                p = obj.Placement
                b = p.Base
                r = p.Rotation
                faces = s.Faces
                #print(dir(faces[0]))
                size_list = len(faces)
                best_face = -1
                lowest_height = 9999999
                for vertex in s.Vertexes:
                    Point = vertex.Point
                    if lowest_height > Point[2]:
                        lowest_height = Point[2]
                #obj.Placement = App.Placement(App.Vector(b[0], b[1], b[2] - lowest_height), r)
                obj.Placement = App.Placement(App.Vector( 0, 0, b[2] - lowest_height), r)

def GetPositionsValues( objs ):
    vertexesAll = []
    positions = []
    CadData = []
    for obj in objs:
        if 'Shape' in dir(obj):
            if str(type(obj)) == "<class 'PartDesign.Body'>":
                # c = obj.Content
                l = obj.Label
                print("{0} Object type = {1}\n".format(l, str(type(obj))))
                p = obj.Placement
                b = p.Base
                positions.append( [ b[ 0 ], b[ 1 ], b[ 2 ] ] )
                vertexes = obj.Shape.Vertexes
                vertexes_list = []
                for vert in vertexes:
                    vertexes_list.append([vert.Point[0], vert.Point[1], vert.Point[2]])
                    try:
                        print('label is {0} content is {1}'.format(l, [vert.Point[0], vert.Point[1], vert.Point[2]]))
                    except:
                        print('label is %s \\n'.format(l))

                vertexesAll.append(vertexes_list)
    return [ positions, vertexesAll ]

def PlaceObjects( objs, values ):
    i = 0
    for obj in objs:
        #print('\n////////////////////////////////////////\nlabel is {0}'.format(q))
        if 'Shape' in dir(obj):
            if str(type(obj)) == "<class 'PartDesign.Body'>":
                s = obj.Shape
                p = obj.Placement
                b = p.Base
                r = p.Rotation

                value = values[ i ]

                spin = makeRotatingPlacement(App.Vector(b[0], b[1], b[2]), App.Vector(0, 0, 1), value[ 1 ])
                obj.Placement = spin.multiply(obj.Placement)

                p = obj.Placement
                b = p.Base
                r = p.Rotation

                obj.Placement = App.Placement(App.Vector(value[ 0 ][ 0 ], value[ 0 ][ 1 ], b[2]), r)
                i += 1

if __name__ == '__main__':
    values = [
        [
            [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]
        ], [
            [
                [0.0, 0.0, 0.0], [0.0, 0.0, 10.000000000000002], [-23.916678999361082, 2.323279862243406, 0.0],
                [-23.916678999361082, 2.323279862243406, 10.000000000000002],
                [-29.93060848686124, -17.32846874629895, 0.0], [-29.93060848686124, -17.32846874629895, 10.000000000000002],
                [-11.41564715505212, -13.622144419362852, 0.0], [-11.41564715505212, -13.622144419362852, 10.000000000000002],
                [-12.324577212391672, -24.22842733639966, 0.0], [-12.324577212391672, -24.22842733639966, 10.000000000000002],
                [1.1786937039936405, -19.678066225809456, 0.0], [1.1786937039936405, -19.678066225809456, 10.000000000000002],
                [-0.7108350385305849, -16.490490181111728, 0.0], [-0.7108350385305849, -16.490490181111728, 10.000000000000002],
                [6.800368513515739, -6.842658830653754, 0.0], [6.800368513515739, -6.842658830653754, 10.000000000000002]
            ],
            [
                [0.0, 0.0, 0.0], [0.0, 0.0, 10.0],
                [14.276848513170684, -19.328133903943268, 0.0], [14.276848513170684, -19.328133903943268, 10.0],
                [32.90504808776189, -10.647768020919079, 0.0], [32.90504808776189, -10.647768020919079, 10.0],
                [17.761785039994063, 0.6315146424835296, 0.0], [17.761785039994063, 0.6315146424835296, 10.0],
                [26.251982227744634, 7.053036493141233, 0.0], [26.251982227744634, 7.053036493141233, 10.0],
                [13.834953058247102, 14.043136512591344, 0.0], [13.834953058247102, 14.043136512591344, 10.0],
                [12.730463928032021, 10.506038313390093, 0.0], [12.730463928032021, 10.506038313390093, 10.0],
                [0.5347517955950347, 9.632291124620764, 0.0], [0.5347517955950347, 9.632291124620764, 10.0]
            ], [
                [0.0, 0.0, 0.0], [0.0, 0.0, 10.000000000000002],
                [-17.98341011951882, 15.937444090881495, 0.0], [-17.98341011951882, 15.937444090881495, 10.000000000000002],
                [-34.39978929173935, 3.573744558465868, 0.0], [-34.39978929173935, 3.573744558465868, 10.000000000000002],
                [-17.242348144524872, -4.31059729198029, 0.0], [-17.242348144524872, -4.31059729198029, 10.000000000000002],
                [-24.211904687886566, -12.35700473594224, 0.0], [-24.211904687886566, -12.35700473594224, 10.000000000000002],
                [-10.612893883471743, -16.612708769293018, 0.0], [-10.612893883471743, -16.612708769293018, 10.000000000000002],
                [-10.26794455789968, -12.923268449631598, 0.0], [-10.26794455789968, -12.923268449631598, 10.000000000000002],
                [1.4795997483194265, -9.532983603107327, 0.0], [1.4795997483194265, -9.532983603107327, 10.000000000000002]
            ], [
                [0.0, 0.0, 0.0], [0.0, 0.0, 10.0],
                [13.970358880484097, 19.550811656482814, 0.0], [13.970358880484097, 19.550811656482814, 10.0],
                [-0.041589899549027365, 34.58490167349741, 0.0], [-0.041589899549027365, 34.58490167349741, 10.0],
                [-6.089299543662626, 16.697312646596103, 0.0], [-6.089299543662626, 16.697312646596103, 10.0],
                [-14.820144960871655, 22.78761062503378, 0.0], [-14.820144960871655, 22.78761062503378, 10.0],
                [-17.631052100900394, 8.81825442196542, 0.0], [-17.631052100900394, 8.81825442196542, 10.0],
                [-13.92576589843533, 8.86084629182341, 0.0], [-13.92576589843533, 8.86084629182341, 10.0],
                [-9.326100633533935, -2.467962472473592, 0.0], [-9.326100633533935, -2.467962472473592, 10.0]
            ], [
                [0.0, 0.0, 0.0], [0.0, 0.0, 10.0],
                [-5.181089807649164, 23.46404637060409, 0.0], [-5.181089807649164, 23.46404637060409, 10.0],
                [-25.729419793007754, 23.11090890900681, 0.0], [-25.729419793007754, 23.11090890900681, 10.0],
                [-16.483058188647846, 6.647451489125526, 0.0], [-16.483058188647846, 6.647451489125526, 10.0],
                [-26.85110750498178, 4.234373674501736, 0.0], [-26.85110750498178, 4.234373674501736, 10.0],
                [-18.35071672644685, -7.201861208110084, 0.0], [-18.35071672644685, -7.201861208110084, 10.0],
                [-15.903048250750661, -4.419797416131349, 0.0], [-15.903048250750661, -4.419797416131349, 10.0],
                [-4.406325830989139, -8.582032653369358, 0.0], [-4.406325830989139, -8.582032653369358, 10.0]
            ]
        ]
    ]

    new_values = TG01_Code.GeneticAlgoV01( 1, 1, 100, values[0], values[1] )

    print("positions = ", new_values )