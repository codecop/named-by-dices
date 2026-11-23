package service;

import java.util.Random;

public final class BuilderIImpl {

    private BuilderIImpl() {
    }

    public static void dummyFactory(BusinessImplDefault manager, int service, int utils) {
        serviceExecutor(manager, service, utils, new int[][] {{1, 0}, {2, 1}, {0, 2}, {1, 2}, {2, 2}});
    }

    public static void factoryDefault(BusinessImplDefault manager, int executor, int factory) {
        serviceExecutor(manager, executor, factory, new int[][] {{0, 0}, {1, 0}, {2, 0}});
    }

    public static void iBusiness(BusinessImplDefault manager, Random data) {
        for (int i = 0; i < manager.businessDefault(); i++) {
            for (int j = 0; j < manager.serviceData(); j++) {
                manager.utilsData(j, i, data.nextBoolean());
            }
        }
    }

    private static void serviceExecutor(BusinessImplDefault grid, int x, int y, int[][] offsets) {
        for (int[] cell : offsets) {
            grid.utilsData(x + cell[0], y + cell[1], true);
        }
    }
}
