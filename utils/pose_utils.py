import numpy as np
PARTS = {
    0: 'NOSE',
    1: 'LEFT_EYE',
    2: 'RIGHT_EYE',
    3: 'LEFT_EAR',
    4: 'RIGHT_EAR',
    5: 'LEFT_SHOULDER',
    6: 'RIGHT_SHOULDER',
    7: 'LEFT_ELBOW',
    8: 'RIGHT_ELBOW',
    9: 'LEFT_WRIST',
    10: 'RIGHT_WRIST',
    11: 'LEFT_HIP',
    12: 'RIGHT_HIP',
    13: 'LEFT_KNEE',
    14: 'RIGHT_KNEE',
    15: 'LEFT_ANKLE',
    16: 'RIGHT_ANKLE'
}

class KeyPoint():
    def __init__(self, index, pos, v):
        x, y = pos
        self.x = x
        self.y = y
        self.index = index
        self.body_part = PARTS.get(index)
        self.confidence = v

    def point(self):
        return int(self.y), int(self.x)

    def to_string(self):
        return 'part: {} location: {} confidence: {}'.format(
            self.body_part, (self.x, self.y), self.confidence)

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def get_keypoints( heatmaps, offsets, output_stride=32):
    scores = sigmoid(heatmaps)
    num_keypoints = scores.shape[2]
    heatmap_positions = []
    offset_vectors = []
    confidences = []
    for ki in range(0, num_keypoints):
        x, y = np.unravel_index(
            np.argmax(scores[:, :, ki]), scores[:, :, ki].shape)
        confidences.append(scores[x, y, ki])
        offset_vector = (offsets[y, x, ki],
                         offsets[y, x, num_keypoints + ki])
        heatmap_positions.append((x, y))
        offset_vectors.append(offset_vector)
    image_positions = np.add(
        np.array(heatmap_positions) *
        output_stride,
        offset_vectors)
    keypoints = [KeyPoint(i, pos, confidences[i])
                 for i, pos in enumerate(image_positions)]
    return keypoints