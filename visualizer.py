import bpy
import numpy as np
import os

class Anton_OT_Visualizer(bpy.types.Operator):
    bl_idname = 'anton.visualize'
    bl_label = 'Anton_Visualizer'
    bl_description = 'Visualizes generated outcome'

    def execute(self, context):
        """Visualizes the generated outcome with metaballs which are implicit surfaces, meaning that they are not explicitly defined
        by vertices. Metaballs are instantiated at the centroid of each element with a density value above the specified threshold.

        :ivar density_out: Density threshold
        :vartype density_out: ``float``
        :ivar cdists: Distance to each element's centroid from origin
        :vartype cdists: *numpy.array* of ``float``
        :ivar coms: Center of mass of each **slice**
        :vartype coms: *numpy.array* of ``float``

        :return: ``FINISHED`` if successful, ``CANCELLED`` otherwise

        \\
        """
        from tqdm import tqdm

        scene = context.scene
        density_out = 0.5

        ecenters = np.load(os.path.join(scene.anton.workspace_path, scene.anton.filename+'.ecenters.npy'))

        if os.path.isfile(os.path.join(scene.anton.workspace_path,
                scene.anton.filename+'_i{}.densities.npy'.format(scene.anton.viz_iteration))):

            densities = np.load(os.path.join(scene.anton.workspace_path, scene.anton.filename+'_i{}.densities.npy'.format(scene.anton.viz_iteration)))
            centroids = ecenters[(densities>density_out)[:, 0]]
            cdists = np.linalg.norm(centroids, axis=1)
            indices = cdists.argsort()

            coms = []
            batch_len = len(indices)//scene.anton.slices

            for _batch in self.batches(centroids[indices], batch_len):
                coms.append(np.mean(_batch, axis=0))

            mball = bpy.data.metaballs.new(scene.anton.filename)
            mball_obj = bpy.data.objects.new(scene.anton.filename+'_i{}.anton'.format(scene.anton.viz_iteration), mball)
            scene.collection.objects.link(mball_obj)

            mball.resolution = 0.05
            mball.render_resolution = 0.05

            currframe = bpy.context.scene.frame_start
            bpy.context.scene.frame_set(currframe)

            anim_len = len(centroids)//scene.anton.keyframes

            for i in tqdm(range(len(indices))):
                melem = mball.elements.new()
                melem.co = coms[i//batch_len]
                melem.radius = scene.anton.metaballrad
                melem.stiffness = scene.anton.metaballsens
                melem.keyframe_insert(data_path='co')

            for i in tqdm(range(len(mball.elements))):
                mball.elements[i].co = centroids[indices[i]]
                mball.elements[i].keyframe_insert(data_path='co', frame=currframe+i//anim_len)

            return {'FINISHED'}
        else:
            return {'CANCELLED'}


    @staticmethod
    def batches(x, n):
        for i in range(0, len(x), n):
            yield x[i:i + n]