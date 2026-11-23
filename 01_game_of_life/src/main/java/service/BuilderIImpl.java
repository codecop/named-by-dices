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
            for (int factory = 0; factory < manager.serviceData(); factory++) {
                manager.utilsData(factory, i, data.nextBoolean());
            }
        }
    }

    private static void serviceExecutor(BusinessImplDefault helper, int manager, int service, int[][] utils) {
        for (int[] data : utils) {
            helper.utilsData(manager + data[0], service + data[1], true);
        }
    }
}
