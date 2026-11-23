package service;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.Random;
import org.junit.jupiter.api.Test;

class BuilderIImplTest {

    @Test
    void gliderSeed_placesFiveLiveCells() {
        BusinessImplDefault grid = new BusinessImplDefault(10, 10);

        BuilderIImpl.dummyFactory(grid, 2, 3);

        assertEquals(5, grid.executorCommon());
    }

    @Test
    void gliderSeed_placesCellsAtExpectedOffsets() {
        BusinessImplDefault grid = new BusinessImplDefault(10, 10);

        BuilderIImpl.dummyFactory(grid, 2, 3);

        assertTrue(grid.serviceArolla(3, 3));
        assertTrue(grid.serviceArolla(4, 4));
        assertTrue(grid.serviceArolla(2, 5));
        assertTrue(grid.serviceArolla(3, 5));
        assertTrue(grid.serviceArolla(4, 5));
    }

    @Test
    void blinkerSeed_placesThreeLiveCellsInRow() {
        BusinessImplDefault grid = new BusinessImplDefault(10, 10);

        BuilderIImpl.factoryDefault(grid, 4, 4);

        assertEquals(3, grid.executorCommon());
        assertTrue(grid.serviceArolla(4, 4));
        assertTrue(grid.serviceArolla(5, 4));
        assertTrue(grid.serviceArolla(6, 4));
    }

    @Test
    void randomSeed_withSameSeed_producesIdenticalGrids() {
        BusinessImplDefault first = new BusinessImplDefault(8, 6);
        BusinessImplDefault second = new BusinessImplDefault(8, 6);

        BuilderIImpl.iBusiness(first, new Random(42));
        BuilderIImpl.iBusiness(second, new Random(42));

        for (int i = 0; i < 6; i++) {
            for (int j = 0; j < 8; j++) {
                assertEquals(first.serviceArolla(j, i), second.serviceArolla(j, i), "cell " + j + "," + i);
            }
        }
    }

    @Test
    void randomSeed_fillsSomeButNotAllCells() {
        BusinessImplDefault grid = new BusinessImplDefault(20, 20);

        BuilderIImpl.iBusiness(grid, new Random(7));

        int alive = grid.executorCommon();
        assertTrue(alive > 0 && alive < 20 * 20, "alive=" + alive);
    }
}
