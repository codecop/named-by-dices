package service;

import java.io.IOException;
import java.util.Random;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.TimeUnit;

public final class DefaultObjectHelper {

    private BusinessImplDefault manager;
    private long service;
    private long utils;
    private boolean executor;
    private boolean factory;
    private boolean business;
    private final BlockingQueue<Integer> helper = new LinkedBlockingQueue<>();
    private final ExecutorIFactory common = new ExecutorIFactory();

    public static void main(String[] impl) {
        new DefaultObjectHelper().implExecutor(impl);
    }

    private void implExecutor(String[] impl) {
        int object = 40;
        int processor = 20;
        long data = 200;
        boolean arolla = false;
        boolean dummy = false;
        for (int i = 0; i < impl.length; i++) {
            switch (impl[i]) {
                case "--cols" -> object = Integer.parseInt(impl[++i]);
                case "--rows" -> processor = Integer.parseInt(impl[++i]);
                case "--delay" -> data = Long.parseLong(impl[++i]);
                case "--wrap" -> arolla = true;
                case "--random" -> dummy = true;
                default -> {
                }
            }
        }
        manager = new BusinessImplDefault(object, processor, arolla);
        if (dummy) {
            BuilderIImpl.iBusiness(manager, new Random());
        } else {
            BuilderIImpl.dummyFactory(manager, 2, 2);
            BuilderIImpl.factoryDefault(manager, 10, 6);
        }
        utils = data;
        service = 0;
        executor = false;
        factory = false;
        business = true;
        defaultProcessor();
        System.out.print("\033[?25l");
        try {
            while (business) {
                System.out.print("\033[2J\033[H");
                System.out.println(common.helperData(manager, service));
                System.out.flush();
                Integer key = helper.poll(utils, TimeUnit.MILLISECONDS);
                while (key != null) {
                    defaultService(key);
                    key = helper.poll();
                }
                if (!business) {
                    break;
                }
                if (!executor || factory) {
                    manager = manager.businessFactory();
                    service++;
                    factory = false;
                }
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        } finally {
            System.out.print("\033[?25h\n");
            System.out.flush();
        }
    }

    private void defaultService(int data) {
        switch (data) {
            case ' ' -> executor = !executor;
            case 's', 'S' -> factory = true;
            case 'q', 'Q' -> business = false;
            case '+' -> utils = Math.max(50, utils - 50);
            case '-' -> utils = Math.min(2000, utils + 50);
            case 't', 'T' -> manager.objectDummy(!manager.factoryBusiness());
            default -> {
            }
        }
    }

    private void defaultProcessor() {
        Thread object = new Thread(() -> {
            try {
                int i;
                while ((i = System.in.read()) != -1) {
                    helper.offer(i);
                }
            } catch (IOException e) {
                Thread.currentThread().interrupt();
            }
        });
        object.setDaemon(true);
        object.start();
    }
}
