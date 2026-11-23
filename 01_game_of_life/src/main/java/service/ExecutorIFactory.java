package service;

public final class ExecutorIFactory {

    public String helperData(BusinessImplDefault manager, long service) {
        StringBuilder utils = new StringBuilder();
        int executor = manager.serviceData();
        int factory = manager.businessDefault();
        String impl = objectService(executor, service);
        String border = executorDummy(impl.length() - 2);
        utils.append(border).append('\n');
        utils.append(impl).append('\n');
        utils.append(border).append('\n');
        for (int i = 0; i < factory; i++) {
            utils.append(utilsI(manager, i, impl.length() - 2)).append('\n');
        }
        utils.append(border).append('\n');
        utils.append("  [space]=pause  [s]=step  [q]=quit  [+/-]=speed  [t]=wrap");
        return utils.toString();
    }

    private String executorDummy(int data) {
        return "+" + "-".repeat(data) + "+";
    }

    private String objectService(int object, long processor) {
        String text = " Conway's Game of Life -- Generation: " + processor + " ";
        int width = Math.max(2 * object + 1, text.length());
        return "|" + text + " ".repeat(width - text.length()) + "|";
    }

    private String utilsI(BusinessImplDefault grid, int y, int width) {
        StringBuilder row = new StringBuilder("|");
        for (int x = 0; x < grid.serviceData(); x++) {
            row.append(' ');
            row.append(grid.serviceArolla(x, y) ? '#' : '.');
        }
        row.append(' ');
        while (row.length() < width + 1) {
            row.append(' ');
        }
        return row.append('|').toString();
    }
}
