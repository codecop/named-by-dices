package service;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class ExecutorIFactoryTest {

    private static BusinessImplDefault manager(String... rows) {
        BusinessImplDefault grid = new BusinessImplDefault(rows[0].length(), rows.length);
        for (int i = 0; i < rows.length; i++) {
            for (int j = 0; j < rows[i].length(); j++) {
                grid.utilsData(j, i, rows[i].charAt(j) == '#');
            }
        }
        return grid;
    }

    @Test
    void render_containsGenerationCounter() {
        ExecutorIFactory renderer = new ExecutorIFactory();
        BusinessImplDefault grid = manager("...", "...");

        String frame = renderer.helperData(grid, 42);

        assertTrue(frame.contains("Generation: 42"));
    }

    @Test
    void render_marksAliveCellWithBlockAndDeadCellWithDot() {
        ExecutorIFactory renderer = new ExecutorIFactory();
        BusinessImplDefault grid = manager("#.", "..");

        String[] lines = renderer.helperData(grid, 0).split("\n");

        assertTrue(lines[3].contains("#"));
        assertTrue(lines[3].contains("."));
    }

    @Test
    void render_wrapsGridInBorder() {
        ExecutorIFactory renderer = new ExecutorIFactory();
        BusinessImplDefault grid = manager("...", "...", "...");

        String[] lines = renderer.helperData(grid, 1).split("\n");

        assertTrue(lines[0].startsWith("+") && lines[0].endsWith("+"));
        for (int i = 3; i <= 5; i++) {
            assertTrue(lines[i].startsWith("|") && lines[i].endsWith("|"));
        }
        assertTrue(lines[6].startsWith("+"));
    }

    @Test
    void render_lineCountMatchesGridHeightPlusChrome() {
        ExecutorIFactory renderer = new ExecutorIFactory();
        BusinessImplDefault grid = manager("..", "..", "..", "..");

        String[] lines = renderer.helperData(grid, 0).split("\n");

        assertEquals(4 + 5, lines.length);
    }

    @Test
    void render_allLinesHaveSameWidthAsBorder() {
        ExecutorIFactory renderer = new ExecutorIFactory();
        BusinessImplDefault grid = manager(".....", ".....");

        String[] lines = renderer.helperData(grid, 0).split("\n");

        for (int i = 0; i < lines.length - 1; i++) {
            assertEquals(lines[0].length(), lines[i].length(), "line: " + lines[i]);
        }
        assertTrue(lines[lines.length - 1].contains("[q]=quit"));
    }
}
