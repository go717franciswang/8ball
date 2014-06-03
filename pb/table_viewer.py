from matplotlib import pyplot as plt
import numpy as np

class TableViewer:
    def display(self, table, block=False):
        img = np.zeros(shape=(table.w, table.h, 3), dtype='uint8')
        img[:,:,1] = np.ones(shape=(table.w, table.h), dtype='uint8') * 255
        plt.imshow(img)
        plt.draw()
        plt.show(block=block)

if __name__ == '__main__':
    import table
    t = table.Table(200, 300)
    table_viewer = TableViewer()
    table_viewer.display(t, True)

