; ModuleID = 'test.ll'
source_filename = "test.c"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

%struct.anon = type { %struct.Type1*, %struct.Type2* }
%struct.Type1 = type { [8 x i8] }
%struct.Type2 = type { i32, i32* }

@.str = private unnamed_addr constant [30 x i8] c"/////This is a Good function\0A\00", align 1
@.str.1 = private unnamed_addr constant [30 x i8] c"/////This is a Evil function\0A\00", align 1
@gvar = dso_local global %struct.anon zeroinitializer, align 8
@.str.2 = private unnamed_addr constant [5 x i8] c"temp\00", align 1
@handler = dso_local global i32 (i32*)* null, align 8
@.str.3 = private unnamed_addr constant [26 x i8] c"crashing path is taken. \0A\00", align 1
@.str.4 = private unnamed_addr constant [38 x i8] c"..........exploiting path is taken. \0A\00", align 1
@global_a = dso_local global i64 0, align 8
@handler1 = dso_local global i32 (i32)* null, align 8
@handler2 = dso_local global i32 (i32)* null, align 8

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @goodFunc(i32* %var) #0 {
entry:
  %call = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([30 x i8], [30 x i8]* @.str, i64 0, i64 0))
  ret i32 0
}

declare dso_local i32 @printf(i8*, ...) #1

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @badFunc(i32* %var) #0 {
entry:
  %call = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([30 x i8], [30 x i8]* @.str.1, i64 0, i64 0))
  ret i32 0
}

; Function Attrs: noinline nounwind uwtable
define dso_local i32 @main(i32 %argc, i8** %argv) #0 {
entry:
  %temp = alloca [16 x i8], align 16
  %array = alloca [10000 x i64], align 16
  %call = call noalias align 16 i8* @malloc(i64 8) #4
  %0 = bitcast i8* %call to %struct.Type1*
  store %struct.Type1* %0, %struct.Type1** getelementptr inbounds (%struct.anon, %struct.anon* @gvar, i32 0, i32 0), align 8
  %call1 = call noalias align 16 i8* @malloc(i64 16) #4
  %1 = bitcast i8* %call1 to %struct.Type2*
  store %struct.Type2* %1, %struct.Type2** getelementptr inbounds (%struct.anon, %struct.anon* @gvar, i32 0, i32 1), align 8
  %arraydecay = getelementptr inbounds [16 x i8], [16 x i8]* %temp, i64 0, i64 0
  call void @klee_make_symbolic(i8* %arraydecay, i64 16, i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.str.2, i64 0, i64 0))
  %arraydecay2 = getelementptr inbounds [16 x i8], [16 x i8]* %temp, i64 0, i64 0
  %2 = load %struct.Type2*, %struct.Type2** getelementptr inbounds (%struct.anon, %struct.anon* @gvar, i32 0, i32 1), align 8
  %status = getelementptr inbounds %struct.Type2, %struct.Type2* %2, i32 0, i32 0
  %3 = bitcast i32* %status to i8*
  call void @llvm.memcpy.p0i8.p0i8.i64(i8* align 8 %3, i8* align 1 %arraydecay2, i64 16, i1 false)
  store i32 (i32*)* @goodFunc, i32 (i32*)** @handler, align 8
  %4 = load %struct.Type2*, %struct.Type2** getelementptr inbounds (%struct.anon, %struct.anon* @gvar, i32 0, i32 1), align 8
  %status3 = getelementptr inbounds %struct.Type2, %struct.Type2* %4, i32 0, i32 0
  %5 = load i32, i32* %status3, align 8
  %tobool = icmp ne i32 %5, 0
  br i1 %tobool, label %if.then, label %if.else

if.then:                                          ; preds = %entry
  %call4 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([26 x i8], [26 x i8]* @.str.3, i64 0, i64 0))
  %6 = load %struct.Type2*, %struct.Type2** getelementptr inbounds (%struct.anon, %struct.anon* @gvar, i32 0, i32 1), align 8
  %ptr = getelementptr inbounds %struct.Type2, %struct.Type2* %6, i32 0, i32 1
  %7 = load i32*, i32** %ptr, align 8
  %8 = load i32, i32* %7, align 4
  br label %if.end

if.else:                                          ; preds = %entry
  %call5 = call noalias align 16 i8* @malloc(i64 8) #4
  %9 = bitcast i8* %call5 to i64*
  %call6 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([38 x i8], [38 x i8]* @.str.4, i64 0, i64 0))
  %10 = load %struct.Type2*, %struct.Type2** getelementptr inbounds (%struct.anon, %struct.anon* @gvar, i32 0, i32 1), align 8
  %ptr7 = getelementptr inbounds %struct.Type2, %struct.Type2* %10, i32 0, i32 1
  %11 = load i32*, i32** %ptr7, align 8
  store i32 4660, i32* %11, align 4
  %12 = load i64, i64* @global_a, align 8
  %sub = sub nsw i64 %12, 100
  %13 = inttoptr i64 %sub to i64*
  %14 = load i64, i64* %13, align 8
  %sub8 = sub nsw i64 %14, 100
  %add = add nsw i64 %sub8, 1000
  %15 = inttoptr i64 %add to i32 (i32*)*
  store i32 (i32*)* %15, i32 (i32*)** @handler, align 8
  br label %if.end

if.end:                                           ; preds = %if.else, %if.then
  %res.0 = phi i32 [ %8, %if.then ], [ undef, %if.else ]
  %16 = load i64, i64* @global_a, align 8
  %17 = inttoptr i64 %16 to i32 (i32*)*
  store i32 (i32*)* %17, i32 (i32*)** @handler, align 8
  br label %for.cond

for.cond:                                         ; preds = %for.inc, %if.end
  %i.0 = phi i32 [ 0, %if.end ], [ %inc, %for.inc ]
  %cmp = icmp slt i32 %i.0, 10000
  br i1 %cmp, label %for.body, label %for.end

for.body:                                         ; preds = %for.cond
  %idxprom = sext i32 %i.0 to i64
  %arrayidx = getelementptr inbounds [10000 x i64], [10000 x i64]* %array, i64 0, i64 %idxprom
  %18 = load i64, i64* %arrayidx, align 8
  %19 = inttoptr i64 %18 to i32 (i32*)*
  store i32 (i32*)* %19, i32 (i32*)** @handler, align 8
  br label %for.inc

for.inc:                                          ; preds = %for.body
  %inc = add nsw i32 %i.0, 1
  br label %for.cond, !llvm.loop !4

for.end:                                          ; preds = %for.cond
  %20 = load i32 (i32*)*, i32 (i32*)** @handler, align 8
  %21 = load %struct.Type2*, %struct.Type2** getelementptr inbounds (%struct.anon, %struct.anon* @gvar, i32 0, i32 1), align 8
  %ptr9 = getelementptr inbounds %struct.Type2, %struct.Type2* %21, i32 0, i32 1
  %22 = load i32*, i32** %ptr9, align 8
  %call10 = call i32 %20(i32* %22)
  ret i32 %res.0
}

; Function Attrs: nounwind
declare dso_local noalias align 16 i8* @malloc(i64) #2

declare dso_local void @klee_make_symbolic(i8*, i64, i8*) #1

; Function Attrs: argmemonly nofree nounwind willreturn
declare void @llvm.memcpy.p0i8.p0i8.i64(i8* noalias nocapture writeonly, i8* noalias nocapture readonly, i64, i1 immarg) #3

attributes #0 = { noinline nounwind uwtable "frame-pointer"="all" "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { "frame-pointer"="all" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #2 = { nounwind "frame-pointer"="all" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #3 = { argmemonly nofree nounwind willreturn }
attributes #4 = { nounwind }

!llvm.module.flags = !{!0, !1, !2}
!llvm.ident = !{!3}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{i32 7, !"uwtable", i32 1}
!2 = !{i32 7, !"frame-pointer", i32 2}
!3 = !{!"clang version 13.0.0 (https://github.com/llvm/llvm-project 35df2f6fbd1ae2e6f9313454e5446212fcbcf90a)"}
!4 = distinct !{!4, !5}
!5 = !{!"llvm.loop.mustprogress"}
