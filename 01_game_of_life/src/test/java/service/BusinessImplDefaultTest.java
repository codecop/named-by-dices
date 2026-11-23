package service;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.HashSet;
import java.util.Set;
import org.junit.jupiter.api.Test;

class BusinessImplDefaultTest {

    private static BusinessImplDefault manager(String... rows) {
        BusinessImplDefault grid = new BusinessImplDefault(rows[0].length(), rows.length);
        for (int i = 0; i < rows.length; i++) {
            for (int j = 0; j < rows[i].length(); j++) {
                grid.utilsData(j, i, rows[i].charAt(j) == '#');
            }
        }
        return grid;
    }

    private static Set<String> factory(BusinessImplDefault grid) {
        Set<String> utils = new HashSet<>();
        for (int i = 0; i < grid.businessDefault(); i++) {
            for (int j = 0; j < grid.serviceData(); j++) {
                if (grid.serviceArolla(j, i)) {
                    utils.add(j + "," + i);
                }
            }
        }
        return utils;
    }

    private static void helper(String[] expected, BusinessImplDefault grid) {
        assertEquals(expected.length, grid.businessDefault());
        assertEquals(expected[0].length(), grid.serviceData());
        for (int i = 0; i < expected.length; i++) {
            for (int j = 0; j < expected[i].length(); j++) {
                assertEquals(expected[i].charAt(j) == '#', grid.serviceArolla(j, i), "cell " + j + "," + i);
            }
        }
    }

    @Test
    void emptyGrid_nextGeneration_staysEmpty() {
        BusinessImplDefault grid = manager("...", "...", "...");

        BusinessImplDefault next = grid.businessFactory();

        assertEquals(0, next.executorCommon());
        helper(new String[] {"...", "...", "..."}, next);
    }

    @Test
    void liveCellWithoutNeighbours_nextGeneration_diesOfUnderpopulation() {
        BusinessImplDefault grid = manager("#..", "...", "...");

        BusinessImplDefault next = grid.businessFactory();

        assertFalse(next.serviceArolla(0, 0));
    }

    @Test
    void liveCellWithTwoNeighbours_nextGeneration_survives() {
        BusinessImplDefault grid = manager("##.", "#..", "...");

        BusinessImplDefault next = grid.businessFactory();

        assertTrue(next.serviceArolla(0, 0));
    }

    @Test
    void liveCellWithThreeNeighbours_nextGeneration_survives() {
        BusinessImplDefault grid = manager("##.", "##.", "...");

        BusinessImplDefault next = grid.businessFactory();

        assertTrue(next.serviceArolla(0, 0));
    }

    @Test
    void liveCellWithFourNeighbours_nextGeneration_diesOfOverpopulation() {
        BusinessImplDefault grid = manager(".#.", "###", ".#.");

        BusinessImplDefault next = grid.businessFactory();

        assertFalse(next.serviceArolla(1, 1));
    }

    @Test
    void deadCellWithExactlyThreeNeighbours_nextGeneration_becomesAlive() {
        BusinessImplDefault grid = manager("##.", "#..", "...");

        BusinessImplDefault next = grid.businessFactory();

        assertTrue(next.serviceArolla(1, 1));
    }

    @Test
    void deadCellWithTwoNeighbours_nextGeneration_staysDead() {
        BusinessImplDefault grid = manager("#..", ".#.", "...");

        BusinessImplDefault next = grid.businessFactory();

        assertFalse(next.serviceArolla(1, 0));
    }

    @Test
    void blinkerPattern_nextGeneration_oscillatesAndReturnsAfterTwoSteps() {
        BusinessImplDefault grid = manager(".....", ".....", ".###.", ".....", ".....");

        BusinessImplDefault vertical = grid.businessFactory();
        helper(new String[] {".....", "..#..", "..#..", "..#..", "....."}, vertical);

        BusinessImplDefault back = vertical.businessFactory();
        helper(new String[] {".....", ".....", ".###.", ".....", "....."}, back);
    }

    @Test
    void gliderPattern_fourGenerations_translatesOneCellDiagonally() {
        BusinessImplDefault grid = manager(
                "..........",
                "..#.......",
                "...#......",
                ".###......",
                "..........");

        BusinessImplDefault current = grid;
        for (int i = 0; i < 4; i++) {
            current = current.businessFactory();
        }

        Set<String> expected = new HashSet<>();
        for (String cell : factory(grid)) {
            String[] xy = cell.split(",");
            expected.add((Integer.parseInt(xy[0]) + 1) + "," + (Integer.parseInt(xy[1]) + 1));
        }
        assertEquals(expected, factory(current));
    }

    @Test
    void cornerCellWithoutWrap_ignoresNeighboursOutsideGrid() {
        BusinessImplDefault grid = manager("#..", "...", "...");

        assertEquals(0, grid.commonUtils(2, 2));
    }

    @Test
    void cornerCellWithWrap_countsNeighboursAcrossBorder() {
        BusinessImplDefault grid = new BusinessImplDefault(3, 3, true);
        grid.utilsData(0, 0, true);

        assertEquals(1, grid.commonUtils(2, 2));
    }

    @Test
    void nextGeneration_doesNotModifyOriginalGrid() {
        BusinessImplDefault grid = manager(".##", "##.", "...");
        Set<String> before = factory(grid);

        grid.businessFactory();

        assertEquals(before, factory(grid));
    }

    @Test
    void aliveCount_countsOnlyLiveCells() {
        BusinessImplDefault grid = manager("#..", ".#.", "..#");

        assertEquals(3, grid.executorCommon());
    }

    @Test
    void setWrap_togglesToroidalNeighbourCounting() {
        BusinessImplDefault grid = manager("#..", "...", "...");

        grid.objectDummy(true);

        assertTrue(grid.factoryBusiness());
        assertEquals(1, grid.commonUtils(2, 2));
    }
}
