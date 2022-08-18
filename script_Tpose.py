# coding=utf-8

# Cette fonction a été réalisée par Guillaume Lebreton et Elliot Janvier pour Solidanim.
# Le but de celle-ci est de mettre un personnage mobu en T-Pose.
#
# -------------------------------------------------------------------------------
# |   _    _ _______ _____ _      _____  _____      _______ _____ ____  _   _   |
# |  | |  | |__   __|_   _| |    |_   _|/ ____|  /\|__   __|_   _/ __ \| \ | |  |
# |  | |  | |  | |    | | | |      | | | (___   /  \  | |    | || |  | |  \| |  |
# |  | |  | |  | |    | | | |      | |  \___ \ / /\ \ | |    | || |  | | . ` |  |
# |  | |__| |  | |   _| |_| |____ _| |_ ____) / ____ \| |   _| || |__| | |\  |  |
# |   \____/   |_|  |_____|______|_____|_____/_/    \_\_|  |_____\____/|_| \_|  |
# |                                                                             |
# | Pour utiliser ce script, il vous faut sélectionner tous les bones excepté   |
# | le root, puis drag and drop le script dans mobu pour l'appliquer. Si il ne  |
# | fonctionne pas bien pour le personnage, il vous suffit de changer la        |
# | template comme indiqué a l'interieur du programme.                          |
# -------------------------------------------------------------------------------

from pyfbsdk import*
lModelList = FBModelList()
FBGetSelectedModels( lModelList )
lScene = FBSystem().Scene

def tPoseAngleMatch( FBVector3d ):
#
#    Cette fonction assigne des valeurs arbitraires a tous les angles qui ne sont pas "droits" automatiquement
#
    for i,angle in enumerate( FBVector3d ):
        negative = False
        if angle < 0 :
            angle = abs( angle )
            negative = True
        if 0 <= angle < 45:
            angle = 0
        elif 45 <= angle < 135:
            angle = 90
        elif 135 <= angle < 225:
            angle = 180
        elif 225 <= angle < 315:
            angle = 270
        elif 315 <= angle :
            angle = 360
        if negative == True :
            angle = -angle
        FBVector3d[i] = angle
    # set angle
    return FBVector3d

def getGlobalRotate( lModel ):

    globalRotation = FBVector3d()
    lModel.GetVector( globalRotation, FBModelTransformationType.kModelRotation, True)
    print "Current Global Rotation:", globalRotation
    return globalRotation 


if len( lModelList ) == 0:
    FBMessageBox( "Message", "Nothing selected", "OK", None, None )
else:
    modifiedmodels = []

#    Ici, on va assigner l'angle déterminé par la fonction au dessus (tPoseAngleMatch), pour les bras et les pouces,
#    l'operation se fait a la main. Si il est necessaire de changer de façon arbitraire les valeurs d'un joint,
#    il suffit de suivre cette template :
#            if model.Name == "nom de votre joint" :
#            tPoseAngle =  FBVector3d( x, y, z)
#      
#    et de la mettre juste en dessous  |
#                                      V
    for model in lModelList:
        print model.Name
        tPoseAngle = tPoseAngleMatch( getGlobalRotate(model) )
#
#        juste ici :)
#
        if model.Name == "arm_stretch.r" :
            tPoseAngle =  FBVector3d( 90, -90, 0)
        if model.Name == "arm_stretch.l" :
            tPoseAngle = FBVector3d( 90, 90, 0)

#       la valeur des deux angles précédents concerne les epaules, selon la conception du rig il faut intervertir les valeurs.

        if model.Name == "c_thumb1.r" :
            tPoseAngle = FBVector3d( -90, 90, 0)
        if model.Name == "c_thumb1.l" :
            tPoseAngle = FBVector3d( 90, 90, 0)
        if model.Name == "c_thumb2.r" :
            tPoseAngle = FBVector3d( -90, 90, 0)
        if model.Name == "c_thumb2.l" :
            tPoseAngle = FBVector3d( 90, 90, 0)
        if model.Name == "c_thumb3.r" :
            tPoseAngle = FBVector3d( -90, 90, 0)
        if model.Name == "c_thumb3.l" :
            tPoseAngle = FBVector3d( 90, 90, 0)
        if model.Name == "c_ring3.r" :
            tPoseAngle = FBVector3d( -90, 90, 0)
        if model.Name == "c_ring3.l" :
            tPoseAngle = FBVector3d( 90, -90, 180)

#       la valeur des angles précédents concerne des phalanges et des valeurs fixes leurs sont appliquées
#       car certaines sont souvent capricieuses. Si vous voulez les ignorer il suffit de les commenter en
#       mettant un "#" au début du couple de lignes qui sont concernées

        model.SetVector( tPoseAngle, FBModelTransformationType.kModelRotation )
        # Refresh the scene after setting transforms
        lScene.Evaluate()
