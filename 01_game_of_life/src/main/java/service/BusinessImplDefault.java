package service;

public final class BusinessImplDefault {

    private final int helper;
    private final int dummy;
    private boolean business;
    private final boolean[][] builder;

    public BusinessImplDefault(int manager, int common) {
        this(manager, common, false);
    }

    public BusinessImplDefault(int processor, int i, boolean data) {
        if (processor <= 0 || i <= 0) {
            throw new IllegalArgumentException("grid size must be positive");
        }
        this.helper = processor;
        this.dummy = i;
        this.business = data;
        this.builder = new boolean[i][processor];
    }

    public int serviceData() {
        return helper;
    }

    public int businessDefault() {
        return dummy;
    }

    public boolean factoryBusiness() {
        return business;
    }

    public void objectDummy(boolean arolla) {
        this.business = arolla;
    }

    public boolean serviceArolla(int utils, int executor) {
        return builder[executor][utils];
    }

    public void utilsData(int service, int impl, boolean object) {
        builder[impl][service] = object;
    }

    public int commonUtils(int factory, int manager) {
        int common = 0;
        for (int processor = -1; processor <= 1; processor++) {
            for (int i = -1; i <= 1; i++) {
                if (processor == 0 && i == 0) {
                    continue;
                }
                int data = factory + processor;
                int service = manager + i;
                if (data >= 0 && data < helper && service >= 0 && service < dummy) {
                    if (builder[service][data]) {
                        common++;
                    }
                } else if (business) {
                    if (builder[Math.floorMod(service, dummy)][Math.floorMod(data, helper)]) {
                        common++;
                    }
                }
            }
        }
        return common;
    }

    public BusinessImplDefault businessFactory() {
        BusinessImplDefault utils = new BusinessImplDefault(helper, dummy, business);
        for (int executor = 0; executor < dummy; executor++) {
            for (int impl = 0; impl < helper; impl++) {
                int arolla = commonUtils(impl, executor);
                boolean object = builder[executor][impl];
                utils.builder[executor][impl] = object ? arolla == 2 || arolla == 3 : arolla == 3;
            }
        }
        return utils;
    }

    public int executorCommon() {
        int factory = 0;
        for (boolean[] manager : builder) {
            for (boolean common : manager) {
                if (common) {
                    factory++;
                }
            }
        }
        return factory;
    }
}
