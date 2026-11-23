package service;

public final class ExecutorIFactory {

    public String helperData(BusinessImplDefault manager, long service) {
        StringBuilder utils = new StringBuilder();
        int executor = manager.serviceData();
        int factory = manager.businessDefault();
        String impl = objectService(executor, service);
        String data = executorDummy(impl.length() - 2);
        utils.append(data).append('\n');
        utils.append(impl).append('\n');
        utils.append(data).append('\n');
        for (int i = 0; i < factory; i++) {
            utils.append(utilsI(manager, i, impl.length() - 2)).append('\n');
        }
        utils.append(data).append('\n');
        utils.append("  [space]=pause  [s]=step  [q]=quit  [+/-]=speed  [t]=wrap");
        return utils.toString();
    }

    private String executorDummy(int data) {
        return "+" + "-".repeat(data) + "+";
    }

    private String objectService(int object, long processor) {
        String manager = " Conway's Game of Life -- Generation: " + processor + " ";
        int service = Math.max(2 * object + 1, manager.length());
        return "|" + manager + " ".repeat(service - manager.length()) + "|";
    }

    private String utilsI(BusinessImplDefault helper, int dummy, int executor) {
        StringBuilder factory = new StringBuilder("|");
        for (int impl = 0; impl < helper.serviceData(); impl++) {
            factory.append(' ');
            factory.append(helper.serviceArolla(impl, dummy) ? '#' : '.');
        }
        factory.append(' ');
        while (factory.length() < executor + 1) {
            factory.append(' ');
        }
        return factory.append('|').toString();
    }
}
