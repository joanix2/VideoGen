import networkx as netx
import numpy as np
import cv2

def create_mesh(depth, image, int_mtx, config):
    H, W, C = image.shape
    ext_H, ext_W = H + 2 * config['extrapolation_thickness'], W + 2 * config['extrapolation_thickness']
    LDI = netx.Graph(H=ext_H, W=ext_W, noext_H=H, noext_W=W, cam_param=int_mtx)
    xy2depth = {}
    int_mtx_pix = int_mtx * np.array([[W], [H], [1.]])
    LDI.graph['cam_param_pix'], LDI.graph['cam_param_pix_inv'] = int_mtx_pix, np.linalg.inv(int_mtx_pix)
    disp = 1. / (-depth)
    LDI.graph['hoffset'], LDI.graph['woffset'] = config['extrapolation_thickness'], config['extrapolation_thickness']
    LDI.graph['bord_up'], LDI.graph['bord_down'] = LDI.graph['hoffset'] + 0, LDI.graph['hoffset'] + H
    LDI.graph['bord_left'], LDI.graph['bord_right'] = LDI.graph['woffset'] + 0, LDI.graph['woffset'] + W
    for idx in range(H):
        for idy in range(W):
            x, y = idx + LDI.graph['hoffset'], idy + LDI.graph['woffset']
            LDI.add_node((x, y, -depth[idx, idy]),
                         color=image[idx, idy],
                         disp=disp[idx, idy],
                         synthesis=False,
                         cc_id=set())
            xy2depth[(x, y)] = [-depth[idx, idy]]
    for x, y, d in LDI.nodes:
        two_nes = [ne for ne in [(x+1, y), (x, y+1)] if ne[0] < LDI.graph['bord_down'] and ne[1] < LDI.graph['bord_right']]
        [LDI.add_edge((ne[0], ne[1], xy2depth[ne][0]), (x, y, d)) for ne in two_nes]
    LDI = calculate_fov(LDI)
    image = np.pad(image,
                    pad_width=((config['extrapolation_thickness'], config['extrapolation_thickness']),
                               (config['extrapolation_thickness'], config['extrapolation_thickness']),
                               (0, 0)),
                    mode='constant')
    depth = np.pad(depth,
                    pad_width=((config['extrapolation_thickness'], config['extrapolation_thickness']),
                               (config['extrapolation_thickness'], config['extrapolation_thickness'])),
                    mode='constant')

    return LDI, xy2depth, image, depth

def calculate_fov(mesh):
    k = mesh.graph['cam_param']
    mesh.graph['hFov'] = 2 * np.arctan(1. / (2*k[0, 0]))
    mesh.graph['vFov'] = 2 * np.arctan(1. / (2*k[1, 1]))
    mesh.graph['aspect'] = mesh.graph['noext_H'] / mesh.graph['noext_W']

    return mesh

def main():
    # Load the depth image
    image_path = "images/image.png"
    depth_image_path = "images/depth_map.png"
    
    image = cv2.imread(image_path).astype(float)
    depth_map = cv2.imread(depth_image_path, cv2.IMREAD_GRAYSCALE).astype(float)
    #depth_image = np.flipud(depth_image)
    
    create_mesh(image, depth_map)
    
if __name__ == "__main__":
    main()